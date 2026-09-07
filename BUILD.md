# Dependencies & Installation

## Build and install from source

This document is the canonical source/manual installation guide for `vhs-decode`, `hifi-decode`, `cvbs-decode`, and `ld-decode` across all supported platforms.

`vhs-decode` is actively developed and tested on recent Ubuntu, Debian, Linux Mint, Windows, and macOS systems (x86 and ARM where supported). Other distributions should also work with equivalent package versions.

There is also a Linux compatibility document with distro-specific notes:
<https://docs.google.com/document/d/132ycIMMNvdKvrNZSzbckXVEPQVLTnH_YX0Oh3lqtkkQ>

If you want portable self-contained binaries instead of source installs, see the wiki guides:

- Linux: <https://github.com/oyvindln/vhs-decode/wiki/Linux-Build>
- Windows: <https://github.com/oyvindln/vhs-decode/wiki/Windows-Build>
- macOS: <https://github.com/oyvindln/vhs-decode/wiki/MacOS-Build>

## Common requirements (all platforms)

- Git
- Python 3.11+
- Rust toolchain (required for decode v0.3.5+)
- FFmpeg

Core Python/runtime dependencies include NumPy, SciPy, Cython, Numba, Pandas, Qt (5/6), Qwt, and CMake build tooling.

Install Rust (Unix shell example):

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
rustc --version
cargo --version
```

## Linux

### Install dependencies

Ubuntu/Debian (adjust package names for your distro):

```bash
sudo apt install curl git qtbase5-dev libqwt-qt5-dev libfftw3-dev libavformat-dev libavcodec-dev libavutil-dev ffmpeg pv pkg-config make cmake sox pipx g++ python3-dev python3-pip
```

Arch Linux:

```bash
sudo pacman -S base-devel git qt5-base qwt fftw ffmpeg pv cmake sox python python-pipx
```

Optional/conditional dependencies:

- HiFi preview mode runtime (`sounddevice`): install PortAudio (`libportaudio2` on Debian/Ubuntu).
- Some Ubuntu 22.04 / Linux Mint 21 systems may also need `libxcb-cursor0` for Qt GUI support.
- Optional GPU FLAC compression tooling:

```bash
sudo apt install make ocl-icd-opencl-dev mono-runtime
```

- Optional FlaLDF package: <https://github.com/TokugawaHeavyIndustries/FlaLDF/releases/tag/v0.1b>

### Build and install with pipx (recommended)

```bash
pipx ensurepath
git clone https://github.com/oyvindln/vhs-decode.git vhs-decode
cd vhs-decode
pipx install .
```

Optional install variants:

```bash
pipx install .[hifi_gui_qt6]
pipx install .[intel]
pipx install --force '.[intel,hifi_gui_qt6]'
```

Optional companion tools:

```bash
pipx install tbc-video-export
```

`tbc-tools` project:
<https://github.com/harrypm/tbc-tools>

### Update an existing pipx install

From inside your `vhs-decode` clone:

```bash
git pull
pipx install --force '.[hifi_gui_qt6]'
```

If you use Intel-specific optimizations:

```bash
pipx install --force '.[intel,hifi_gui_qt6]'
```

If activation scripts in the pipx venv are not writable:

```bash
chmod u+w ~/.local/pipx/venvs/vhs-decode/bin/activate ~/.local/pipx/venvs/vhs-decode/bin/activate.csh ~/.local/pipx/venvs/vhs-decode/bin/activate.fish ~/.local/pipx/venvs/vhs-decode/bin/Activate.ps1
pipx reinstall vhs_decode --python python3
```

### Build and install in a Python virtual environment

```bash
python3 -m venv vhs_decode_venv
source ./vhs_decode_venv/bin/activate
git clone https://github.com/oyvindln/vhs-decode.git vhs-decode
cd vhs-decode
python -m pip install --upgrade pip
python -m pip install .[hifi_gui_qt6]
```

## Windows

Windows setup/usage wiki:
<https://github.com/oyvindln/vhs-decode/wiki/Windows-Build>

### Install dependencies

1. Install Python 3.11+ from <https://www.python.org/downloads/>.
   - Check the box to add Python to `PATH`.
   - If a new major Python release is not yet supported by `numba`, use the latest supported version.
2. Install Visual Studio Build Tools 2022 (Desktop development with C++).
3. Install Rust from <https://www.rust-lang.org/tools/install>.

### Manual quick build notes (Windows native)

This keeps the original quick manual path in one place:

1. Install Python 3.13 (or the latest `numba`-supported Python release).
2. Install Visual Studio Build Tools 2022.
3. Install Rust.
4. Clone `vhs-decode`, enter the repo folder, then install:

```powershell
pip install .[hifi_gui_qt6]
```

5. Example source-tree launch:

```powershell
python C:\path\to\vhs-decode\decode.py hifi --gui
```

### Build and install in a Python virtual environment

PowerShell:

```powershell
py -m venv vhs_decode_venv
.\vhs_decode_venv\Scripts\Activate.ps1
git clone https://github.com/oyvindln/vhs-decode.git vhs-decode
cd vhs-decode
py -m pip install --upgrade pip
py -m pip install .[hifi_gui_qt6]
```

CMD activation command:

```cmd
.\vhs_decode_venv\Scripts\activate.bat
```

### Update a virtualenv install

```powershell
cd vhs-decode
git pull
py -m pip install --upgrade --force-reinstall .[hifi_gui_qt6]
```

## macOS

macOS setup/usage wiki:
<https://github.com/oyvindln/vhs-decode/wiki/MacOS-Build>

### Install dependencies (Homebrew)

```bash
brew install cmake pkg-config qt qwt ffmpeg fftw python pipx rust portaudio
```

### Build and install with pipx

```bash
pipx ensurepath
git clone https://github.com/oyvindln/vhs-decode.git vhs-decode
cd vhs-decode
pipx install .
pipx install tbc-video-export
```

Optional install variants:

```bash
pipx install .[hifi_gui_qt6]
pipx install .[intel]
pipx install --force '.[intel,hifi_gui_qt6]'
```

### Build and install in a Python virtual environment

```bash
python3 -m venv vhs_decode_venv
source ./vhs_decode_venv/bin/activate
git clone https://github.com/oyvindln/vhs-decode.git vhs-decode
cd vhs-decode
python -m pip install --upgrade pip
python -m pip install .[hifi_gui_qt6]
```

## HiFi decode notes (important)

- HiFi preview mode requires PortAudio available on the system for source installs.
- Standard FLAC inputs with correct header/context should decode directly without `--raw_format` overrides.
- For long RF FLAC captures where FLAC STREAMINFO sample count metadata is truncated/wrapped, `hifi-decode` falls back to external decoders for full-length reads.
- Keep at least one external decoder available in `PATH`:
  - `flac` (preferred fallback)
  - `ffmpeg` (fallback when `flac` is unavailable)
- Use overrides only when needed:
  - `--frequency` when your RF input rate is not the default 40 MHz.
  - `--raw_format` for stdin (`-`) or when you intentionally need precision override behavior.

Standard FLAC decode example:

```bash
hifi-decode <input.flac> <output.flac>
```

## Verify installation

Run in your normal shell (or activated venv):

```bash
vhs-decode --version
hifi-decode --version
decode-launcher --help
```

## Nix (not fully tested in this repo)

```bash
nix build
nix run
nix run .#ld-decode
nix run .#ld-ldf-reader-py
nix develop
```
