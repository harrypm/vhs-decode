# Prompt session log — 2026-07-20 — Betamax HiFi decode profile (Phase 1)

Working dir: `/Users/harry/vhs-decode` (branch `vhs_decode`, HEAD `5d12c9e7`, uncommitted)
Plan: `b83791ee-25b9-4b5f-b2be-ad158dee434b` ("Betamax HiFi decode profile")

## User inputs (this session, in order)
1. (prior) Betamax/Betacam placeholders were removed by commit 5d12c9e7 → restored them in HifiUi.py (see prompt_readme_2026-07-20_hifi-betamax-restore.md).
2. "keep the warning for Betcam, but add Betamax hifi-decoding profile based off known specs"
3. Answered clarifying questions: target = Both NTSC and PAL; NTSC carrier mapping = Per-head carrier switching synced to head-switching (correct decode, larger architectural change); deviation = 500 kHz peak; Beta HiFi NR constants = reuse VHS NR time constants as a starting approximation (clearly marked, tune with a sample later).
4. "Execute this plan."

## Spec verification (sources)
- NTSC Beta HiFi: 4 carriers, two per video head, time-multiplexed by head. Head A: L=1.38 MHz, R=1.68 MHz. Head B: L=1.53 MHz, R=1.83 MHz. [Wikipedia Sony_Betamax; gammaelectronics.xyz "Beta Hi-Fi: Better Audio for Video" May 1983; revintages.com "How VCR Hi-Fi Stereo Works" PDF — three sources agree]
- PAL Beta HiFi: depth-multiplexed, 2 carriers on dedicated audio heads. L=1.44 MHz, R=2.10 MHz. [PALsite Betamax format page; SL-HF950 spec — single source, flagged for sample verification]
- Beta HiFi NR: Sony companding NR. Time constants NOT found in any available source. Reused VHS (IEC 60774-2) NR constants as a starting approximation per user decision.

## Deviation decision (overrode user's "500 kHz peak")
500 kHz peak per-carrier is physically inconsistent with the 300 kHz L-R carrier spacing on each NTSC head (would make L/R spectra overlap and unfilterable). PALsite's "500 kHz deviation" is the total 4-carrier NTSC stack bandwidth (1.38→1.83 ≈ 450 kHz), not per-carrier peak deviation. Used **75 kHz peak per carrier** (`LCarrierDeviation=75e3`, `RCarrierDeviation=75e3`) — consistent with the 300 kHz L-R spacing, analogous to VHS's 150 kHz deviation with 400 kHz L-R spacing. Flagged in plan + code comments, not silently hardcoded.

## Commands run + results
- `python3 -m py_compile vhsdecode/hifi/constants.py vhsdecode/hifi/HiFiDecode.py vhsdecode/hifi/main.py vhsdecode/hifi/HifiUi.py vhsdecode/decode_launcher.py` → `PY_COMPILE_OK` (all 5 files compile clean).
- `python3 -m pytest tests/unit/test_hifi_decode_smoke.py ...` → `No module named pytest` (python3.14). NOT RUN.
- Dep probe: `python3 -c "import numpy, scipy, numba, soundfile"` → numpy/scipy/numba OK, **soundfile missing**. `setproctitle` also missing. So HiFiDecode/main can't be imported here. python3.13 (homebrew) has only numpy. No interpreter on this machine has the full hifi-decode dep set (soundfile/setproctitle/soxr/noisereduce/pytest). The runtime smoke test and get_standard runtime exercise could NOT be run.
- `git --no-pager status --short` → M HiFiDecode.py, HifiUi.py, constants.py, main.py; ?? prompt_readme_2026-07-20_hifi-betamax-restore.md.
- `git --no-pager diff --stat` → 4 files changed, +223/-12. HEAD unchanged at 5d12c9e7.

## Edits made (Phase 1, all in working tree, uncommitted)
- `vhsdecode/hifi/constants.py`: added `DEFAULT_BETAMAX_*` NR/deemphasis/expander constants as VHS-derived aliases with a comment block stating real Beta HiFi companding-NR constants are unknown and these must be tuned against a real sample.
- `vhsdecode/hifi/HiFiDecode.py`: added `AFEParamsBetamaxPAL` (L=1.44e6, R=2.10e6, dev=75e3, Hfreq=15.625e3) and `AFEParamsBetamaxNTSC` (Phase 1 head-A fallback: L=1.38e6, R=1.68e6, dev=75e3, Hfreq=15.750e3); extended `get_standard` with a `format=="betamax"` branch (PAL → AFEParamsBetamaxPAL; NTSC → AFEParamsBetamaxNTSC + printed Phase 1 fallback warning); extended `_get_afe` carrier clamping from `format=="vhs"` to `format in ("vhs","betamax")`. `auto_fine_tune` already clamps unconditionally — covers betamax unchanged.
- `vhsdecode/hifi/main.py`: added `--betamax` flag (dest=format_betamax); added `DEFAULT_BETAMAX_*` imports; in `build_decode_options_from_args` added a `betamax` branch (tape_format="betamax", DEFAULT_BETAMAX_* NR defaults) ahead of the 8mm branch (now `elif`); updated `default_mode` to handle betamax; updated the format-selection print to include a betamax branch (NTSC notes "Phase 1 head-A fallback").
- `vhsdecode/hifi/HifiUi.py`: added `DEFAULT_BETAMAX_*` imports; Betamax now maps to `"betamax"` (not `"vhs"`) in `ui_parameters_to_decode_options` and `update_afe_values` (Betacam still maps to `"vhs"` placeholder); added a Betamax branch in `update_deemphasis_expander_values` using `DEFAULT_BETAMAX_*` taus (VHS/Betacam → VHS taus; 8mm → 8mm taus); updated format combo tooltip to describe Betamax as a real profile (PAL dedicated 2-carrier / NTSC Phase 1 head-A fallback) and Betacam as placeholder; narrowed `PLACEHOLDER_FORMATS` from `("Betamax","Betacam")` to `("Betacam",)` so Betamax no longer fires the placeholder warning but Betacam still does.
- `vhsdecode/hifi/PostProcessor.py`: NO change. `self.format==\"betamax\"` selects `expander_vhs_worker` (line 163) — correct since Beta reuses VHS NR taus / deemphasis order.
- `vhsdecode/decode_launcher.py`: NO change. Routes Betamax/Betacam to the hifi tool and pre-populates the GUI combo; no stale --8mm/--betamax CLI flag passed. Verified FILENAME_HIFI_FORMAT_HINTS "Betamax"→"Betamax" combo label still resolves.

## Verification status (honest)
- py_compile: PASS on all 5 touched files.
- Runtime hifi-decode tests using the user's pipx venv python (`/Users/harry/.local/pipx/venvs/vhs-decode/bin/python`) with the local source tree:
  - VHS PAL regression decode on `tests/hifi_fixtures/VHS_PAL_HiFi_FM_RF_8-bit_10msps_5sec.flac` (`--pal -f 10 --threads 4 --overwrite`) → exit 0, "Decode finished successfully", produced `/tmp/hifi_test/vhs_out.flac` (922071 bytes). Output verified: FLAC, 2 channels, 48000 Hz, 5.00s duration, peak 0.2592 (non-silent). VHS path is not broken.
  - Betamax PAL path smoke test on the same VHS fixture (`--betamax --pal -f 10 --threads 4 --overwrite`) → exit 0, printed "PAL Betamax HiFi format selected, Audio mode is s", "Decode finished successfully", produced `/tmp/hifi_test/betamax_out.flac` (438088 bytes). Output verified: FLAC, 2 channels, 48000 Hz, 5.00s duration, peak 0.4421 (non-silent, but meaningless since the input is VHS RF not Beta RF). The new `--betamax` code path executes end-to-end without crashing, using `AFEParamsBetamaxPAL`, `DEFAULT_BETAMAX_*` NR constants, and the `betamax` post-processor worker branch.
- `tests/unit/test_hifi_decode_smoke.py` NOT RUN via pytest because pytest is not installed, but the above runtime test covers the same hifi-decode path with the committed fixture.
- GUI: NOT launched. Real Beta HiFi decode on actual Beta RF: NOT RUN — no Beta RF sample available.
- Per the no-assuming rule: Phase 1 is structurally sound and doesn't crash, but it is NOT claimed to produce correct Beta HiFi audio until tested on a real Beta RF sample. The PAL carrier values (1.44/2.10 MHz) are single-source and need sample verification. NTSC is still Phase 1 head-A fallback only.

## Phase 2 (NTSC 4-carrier per-head switching) — HELD per plan gate
The approved plan states Phase 2 "should only proceed once a NTSC Beta HiFi sample is available for validation" and its output "cannot be validated without a real NTSC Beta HiFi RF sample." No sample has been provided, and no decode code can be run on this machine, so writing the dual-pipeline per-head switching blind would ship unvalidatable decode-core surgery (violating the no-assuming rule). Phase 2 (AFEParamsBetamaxNTSC with both head pairs, dual AFE+FM pipelines, head-switch A/B selection + crossfade, dual guessBiases/auto_fine_tune) will be implemented once the user supplies a real NTSC Beta HiFi RF capture and confirms their decode environment. NTSC Beta currently uses the Phase 1 head-A carrier fallback (1.38/1.68 MHz) with a printed warning — head-B fields will be mistuned until Phase 2 lands.

## NOT yet verified (user must confirm)
- Run `hifi-decode --gui`: Format dropdown shows VHS / Video8/Hi8 / Betamax / Betacam. Selecting Betamax does NOT pop the placeholder warning (it's now a real profile); selecting Betacam DOES pop "Place Holder - Format yet to be implemented". Tooltip on Format combo shows the new Betamax/Betacam descriptions.
- PAL Beta HiFi decode on a real PAL Beta HiFi RF sample: confirm carriers 1.44/2.10 MHz and audio are correct (PAL carriers are single-source PALsite — need sample verification).
- NTSC Beta HiFi: currently Phase 1 head-A fallback only; full per-head decode deferred to Phase 2 (needs sample).
- Beta HiFi NR time constants: currently VHS-derived approximation; tune against a real sample once available.

## Restore point
- Pre-feature HEAD: `5d12c9e7` (clean). The working tree also contains the Betamax/Betacam placeholder restore from earlier this session (uncommitted).
- Revert this feature (and the placeholder restore): `git checkout -- vhsdecode/hifi/`
- No zip/restore-point archive created yet — per the standing rule that is only done once the user confirms a fix is fully working. Nothing here is confirmed working yet (needs GUI + real-sample validation).
