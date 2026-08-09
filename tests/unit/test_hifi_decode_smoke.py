"""Smoke / regression test for the HiFi decode pipeline.

Runs ``hifi-decode`` end-to-end on a real VHS/PAL HiFi FM RF capture and
asserts it completes without crashing and produces a valid, non-silent
stereo FLAC.

Regression target: on Linux, when ``libnuma`` is available, ``NUMA.bind_process``
called the libnuma bitmask API through ``ctypes`` without declaring ``restype``
for ``numa_allocate_nodemask``. The default ``c_int`` restype truncated the
returned 64-bit ``struct bitmask *`` pointer to 32 bits, so the subsequent
``numa_bitmask_*`` calls dereferenced an invalid pointer and the process
died with ``SIGSEGV`` (exit 139). This only manifested on Linux (direct
build and AppImage) because Windows has no ``libnuma`` and skips the NUMA
path entirely. The decode is run in a subprocess so a re-introduced crash
shows up as a non-zero exit code (139 / -11) rather than killing the
pytest worker.

The fixture lives in ``tests/hifi_fixtures/`` (committed to this repo)
rather than ``tests/data`` (a git submodule pointing at an external
testdata repository that cannot hold this capture). The test falls back
to ``tests/data`` if the fixture is later mirrored into the submodule.
"""
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

FIXTURE_NAME = "VHS_PAL_HiFi_FM_RF_8-bit_10msps_5sec.flac"


# Primary fixture location: committed directly in this repo (not in the
# tests/data submodule, which points at an external testdata repository).
_FIXTURE_DIR = Path(__file__).resolve().parents[1] / "hifi_fixtures"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resolve_fixture(data_dir: Path) -> Path | None:
    committed = _FIXTURE_DIR / FIXTURE_NAME
    if committed.is_file():
        return committed
    # fallback: the tests/data submodule, if it has been populated
    submod = data_dir / FIXTURE_NAME
    if submod.is_file():
        return submod
    return None


def test_hifi_decode_runs_without_crashing(tmp_path, data_dir):
    fixture = _resolve_fixture(data_dir)
    if fixture is None:
        pytest.skip(
            f"HiFi smoke fixture not present in {_FIXTURE_DIR} or {data_dir}"
        )

    out_file = tmp_path / "hifi_decoded.flac"
    argv = [
        "--pal",
        "-f",
        "10",
        "--threads",
        "1",
        "--overwrite",
        str(fixture),
        str(out_file),
    ]

    # Run in a subprocess with cwd at the repo root so the source tree's
    # vhsdecode package is imported (shadowing any installed copy). A
    # segfault in the child surfaces as returncode 139 / -11.
    script = (
        "import sys\n"
        "from vhsdecode.hifi import main as hifi_main\n"
        f"sys.exit(hifi_main.main({argv!r}))\n"
    )
    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    env.setdefault("QT_QPA_PLATFORM", "offscreen")

    proc = subprocess.run(
        [sys.executable, "-c", script],
        cwd=str(_repo_root()),
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )

    tail = (
        f"\n--- stdout (tail) ---\n{proc.stdout[-2000:]}"
        f"\n--- stderr (tail) ---\n{proc.stderr[-2000:]}"
    )
    assert proc.returncode == 0, (
        f"hifi-decode exited with {proc.returncode} (crash/segfault "
        f"if 139 or -11){tail}"
    )

    assert out_file.is_file(), f"no output file produced at {out_file}"
    assert out_file.stat().st_size > 0, f"output file is empty: {out_file}"

    # Validate the output is a real stereo FLAC with audio content.
    with sf.SoundFile(str(out_file)) as f:
        assert f.format == "FLAC", f"unexpected output format: {f.format}"
        assert f.channels == 2, f"expected stereo, got {f.channels} channels"
        assert f.samplerate == 48000, f"expected 48kHz, got {f.samplerate}"
        # 5 s capture should decode to roughly 5 s of audio (allow slack).
        duration = f.frames / f.samplerate
        assert 4.0 <= duration <= 6.0, f"unexpected decode duration: {duration:.2f}s"
        data = f.read(frames=4096)

    assert data.size > 0, "decoded buffer is empty"
    peak = float(np.max(np.abs(data)))
    assert peak > 0.0, "decoded audio is silent (peak amplitude 0)"
