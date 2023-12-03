![vhs-decode logo](docs/vhs-decode_logo_256px.png)


# VHS-Decode (It does more than VHS now!)


Tape decoding fork of [LD-Decode](https://github.com/happycube/ld-decode), the decoding software powering the [Domesday86 Project](https://www.domesday86.com/).  

This version has been modified to work with the differences found in the tracked RF drum head signals taken directly from colour-under & composite modualted magnetic tape formats.

[FAQ - Frequently Asked Questions](https://github.com/oyvindln/vhs-decode/wiki/FAQ)


Example Videos: [VHS-Decode](https://odysee.com/@vhs-decode:7) / [The Rewinding](https://odysee.com/@therewinding:4?view=content) - Odysee / [The Video Dump Channel](https://www.youtube.com/@videodumpchannel) - YouTube

(Not to be confused with the TV Modulator/Demodulator pack or the **"antenna connectors"** on the back of the VCR!).

<img src="https://github.com/harrypm/vhs-decode/assets/56382624/8a9d7e97-fdf6-4b68-80db-118aea1488dd" width="800" height="">


# CVBS-Decode - Composite Video Decoder


[Wiki Page](https://github.com/oyvindln/vhs-decode/wiki/CVBS-Composite-Decode)


<img src="https://github.com/harrypm/vhs-decode/assets/56382624/d9aab894-b788-4d9c-9f97-ae57ccf5b988" width="800" height="">


This repository also contains an **experimental** CVBS decoder, `cvbs-decode`, which shares code with ld-decode and vhs-decode. Capable of decoding basic raw digitized NTSC and PAL composite video, including colour if the source is somewhat stable. 

# HiFi-Decode & RTLSDR-Decode

Thanks to VideoMem's work on [Superheterodyne Decoding Tools](https://github.com/VideoMem/Superheterodyne-decoding-tools) we now have a working [HiFi Audio Decoder](https://github.com/oyvindln/vhs-decode/wiki/003-Audio) which provides decoding for (S)VHS, Betamax, Video8 & Hi8 HiFi FM tracks.

- 24-bit 192khz FLAC stereo files. 
- Software Noise Reduction 

[RTLSDR Decode](https://github.com/oyvindln/vhs-decode/wiki/RTLSDR) can run in realtime (1~3 sec delay) and provide live playback 8msps RF files and a 48khz 24-bit FLAC file of the decoded audio.


# [Supported Formats](https://github.com/oyvindln/vhs-decode/wiki/Tape-Format-Support-List)


## Tape:


| Format                 | Format Type         | Line  System  | TV System                    | Level of Decoding Support     | RF Capture Support | HiFi Decoding Support |
|------------------------|---------------------|---------------|------------------------------|-------------------------------|--------------------|-----------------------|
| (S)VHS                 | Colour-Under        | 525 & 625     | NTSC, NTSC-J, PAL, PAL-M     | High                          | Yes, Standerdised  | High                  | 
| Betamax                | Colour-Under        | 525 & 625     | NTSC, PAL                    | Medium                        | Yes, Standerdised  | Medium                | 
| U-Matic Low Band       | Colour-Under        | 525 & 625     | NTSC, PAL                    | High                          | Yes, Standerdised  | N/A - Linear Audio    |
| U-Matic (SP) High Band | Colour-Under        | 525 & 625     | PAL                          | High                          | Yes, Standerdised  | N/A - Linear Audio    |
| Video8 & Hi8           | Colour-Under        | 525 & 625     | NTSC, PAL                    | Medium (Chroma needs work)    | Yes, Standerdised  | Medium                |
| Philips VCR            | Colour-Under        | 525 & 625     | NTSC, PAL                    | Medium                        | Yes, Standerdised  | N/A - Linear Audio    |
| EIAJ                   | Colour-Under        | 405, 525, 625 | PAL (NTSC Samples Needed)    | Medium                        | Yes, Standerdised  | N/A - Linear Audio    |
| SMPTE-C 1" Type C      | Modulated Composite | 525 & 625     | NTSC, PAL                    | Medium (More Samples Needed)  | Yes, Standerdised  | N/A - Linear Audio    | 
| SMPTE-B 1" Type B      | Modulated Composite | 525 & 625     | NTSC, PAL                    | Work In Progress              | Yes, Standerdised  | N/A - Linear Audio    | 
| 2" Quadduplex          | Modulated Composite | 525, 625, 655 | NTSC, PAL                    | Samples Required              | Work In Progress   | N/A - Linear Audio    |



## LaserDisc:


| Format            | Format Type         | Line System  | TV System                 | Level of Decoding Support | RF Capture Support    |
|-------------------|---------------------|--------------|---------------------------|---------------------------|-----------------------|
| LaserDisc CAV     | Composite Modulated | 525 & 625    | NTSC, NTSC-J, PAL, PAL-M  | High                      | Yes, Standerdised     |
| LaserDisc CLV     | Composite Modulated | 525 & 625    | NTSC, NTSC-J, PAL, PAL-M  | High                      | Yes, Standerdised     |
| LaserDisc MUSE    | Composite Modulated | 1125         | HDTV                      | Not Implimented           | Work In Prgress       |


## Composite:


| Signal Format | Resolution | Field System | TV System | Aspect Ratio | RF Capture Support | Video Decoding Support |
|---------------|------------|--------------|-----------|--------------|--------------------|------------------------|
| CVBS          | 525 Lines  | Interlaced   | 525 NTSC  | 4:3 / 16:9   | Yes*               | Yes*                   |
| CVBS          | 625 Lines  | Interlaced   | 625 PAL   | 4:3 / 16:9   | Yes*               | Yes*                   |
| CVBS          | 405 Lines  | Interlaced   | 405 PAL   | 4:3          | Yes*               | Not Tested/Implimented |
| CVBS          | 819 Lines  | Interlaced   | 405 PAL   | 4:3          | Yes*               | Not Tested/Implimented |
| CVBS 240p     | 240 Lines  | Progressive  | NTSC      | 4:3 / 16:9   | Yes*               | Work in Progress       |
| CVBS 288p     | 288 Lines  | Progressive  | PAL       | 4:3 / 16:9   | Yes*               | Work in Progress       |
| 960h CCTV     | 960 x 576  | Interlaced   | N/A       | 16:9 Only    | Yes*               | Not Tested             |


*RAW CVBS has been captured using CX Cards & CXADC, however, only at lowest gain states, CVBS capture is not possible with the DomesDayDuplicator Rev3 due to input filtering on the hardware.


# Oprating System Support


VHS-Decode, as with LD-Decode, has been developed and tested on machines running the latest versions of Ubuntu, Debian, Linux Mint.

Other distributions might have outdated (or even newer) versions of certain Python libraries or other dependencies, breaking compatibility.

Other dependencies include Python 3.8+, numpy, scipy, cython, numba, pandas, Qt5, Cmake, and FFmpeg.


## Windows


[Windows Setup & Downloads](https://github.com/oyvindln/vhs-decode/wiki/Windows-Build)

The ld-tools suit alongside a combined exe version of `ld-decode` / `vhs-decode` / `cvbs-decode` / `hifi-decode` inside a single `decode.exe` has been ported to windows. 

This allows the use of ld-analyse to view TBC files and ld-lds-converter to convert and compress DdD captures inside Windows with drag and drop bat scripts video exporting also has an export script, hifi decoding is currently only avalible via WSL2 or via RTLSDR decode via GNURadio.

[Windows Sub-System For Linux - WSL2 Setup](https://github.com/oyvindln/vhs-decode/wiki/WSL2-Setup)

Its fully working on WSL2 20.04 & 22.04.1 LTS (Windows Subsystem for Linux) however issues with larger captures i.g 180gb+ may require expanding the default [virtual disk size](https://docs.microsoft.com/en-us/windows/wsl/vhd-size).


## MacOS


Due to developers not having a range of apple systems, this is entirely tested by community members.

[MacOS Build](https://github.com/oyvindln/vhs-decode/wiki/MacOS-Build) currently install docs are only for ARM based apple products such as the M1/M2/M3 lines and newer devices.


## Linux


[Linux compatability doc](https://docs.google.com/document/d/132ycIMMNvdKvrNZSzbckXVEPQVLTnH_YX0Oh3lqtkkQ/edit) for various tested distributions of Linux.



Installation on Linux (Ubuntu/Debian-based)

Install all dependencies required by LD-Decode & VHS-Decode:

    sudo apt install clang python3-setuptools python3-numpy python3-scipy python3-matplotlib git qt5-default libqwt-qt5-dev libfftw3-dev python3-tk python3-numba libavformat-dev libavcodec-dev libavutil-dev ffmpeg openssl pv python3-distutils make cython3 cmake pipx

For Ubuntu 22.04 that is:

    sudo apt install clang python3-setuptools python3-numpy python3-scipy python3-matplotlib git qt5-qmake qtbase5-dev libqwt-qt5-dev libfftw3-dev python3-tk python3-numba libavformat-dev libavcodec-dev libavutil-dev ffmpeg openssl pv python3-distutils pkg-config make cython3 cmake pipx

Set up pipx

    pipx ensurepath

(Alternatively, a [python virtual environment](https://docs.python.org/3/library/venv.html) can be used instead of using pipx)

Optional dependencies for GPU (Nvidia Cards) FLAC compression support:

    sudo apt install make ocl-icd-opencl-dev mono-runtime


## Build VHS-Decode & LD-Tools Suite


The vhs-decode respository also has hifi-decode, cvbs-decode, ld-decode included.

Download VHS-Decode:

    git clone https://github.com/oyvindln/vhs-decode.git vhs-decode

Install VHS-Decode:

    cd vhs-decode

Build and install vhs-decode via pipx

    pipx install .

Compile and Install ld-tools suite: (Required)

    mkdir build2
    cd build2
    cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_QT_VERSION=5
    make -j4
    sudo make install
   

Go back to the main directory with 

    cd .. 

To update do `git pull` while inside of the vhs-decode directory.
To update to the latest git version of vhs-decode/ld-decode/hi-fi decode, run `pipx install .` inside the vhs-decode directory after running `git pull`
To update the tools to the latest version, the steps under "Compile and Install ld-tools suite: (Required)" has to be re-ran after a `git pull`. The tools are not updated very often.

**Note:** debian/ubuntu does not have a qt6 version of qwt in repositories as of yet so you have to inform the build script to use Qt5 if both qt5 and qt6 are installed with -DUSE_QT_VERSION=5 as it might otherwise try to compile with qt6 instead and failing to locate qwt. The option is otherwise not needed.



# Step 01 Aquire a working VCR or VTR


Almost any VCR or VRT will work for FM RF capture.

Preferably within spec and in excellent mechanical and head condition, for VHS metal track decks are somewhat preferable as they were built generally better in terms of mechnical stability than cheaper later consumer decks that use more plastics, however in any and all cases only **crtical requirement** is avalible test points or a head amplifyer that is easy to tap into, this goes for any and all tape formats, if the deck can track your tape it can be used for FM RF capture 90% of the time.

**Note** SVHS tapes can be RF captured on standard VHS HiFi decks.

**Note** SVHS NTSC Decks - Currently inflated, but you can import PAL decks with NTSC support for 1/3rd the price though this only applys if conventional refrance SVHS captures are required.

**Always clean your tape track/drum/heads** before and afterwards with 99.9% isopropanol and lint free cloths/pads/paper. This ensures less dropouts from dirty heads or tracks including the track of the head drum but its alway good practice to avoid cross contamination of tapes.

We have a [Cleaning & Servicing Guide](https://github.com/oyvindln/vhs-decode/wiki/Cleaning-&-Servicing-Guide) a poorly mantained VCR is always going to perform poorly do not run valuable tapes though VCRs that have not been inspected.


# Step 2: Aquire an RF Capture Device


Currently standardised is 3 devices [**but RF capture is not limited to these devices only**]().

<img src="https://github.com/oyvindln/vhs-decode/wiki/assets/images/Hardware/DdD-Rev3-CX-White-Sony-ILCE-7RM3-2022.12.20-21.54.48.png" width="600" height="">

## [Domesday Duplicator (DdD)](https://github.com/harrypm/DomesdayDuplicator#readme) (300-350USD*)

Capture is done using an simple GUI application.

[Linux Application](https://github.com/harrypm/DomesdayDuplicator#readme) / [Windows Application](https://github.com/TokugawaHeavyIndustries/DomesdayDuplicator-WinBuild/releases/) / [MacOS Application](https://github.com/harrypm/DomesdayDuplicator#macos-software-installation)

Originally geared towards capturing RF from Laserdisc players, it does however also work perfectly well for digitizing tape RF data. It consists of a custom analogue to digital board with an amplifier, an off-the-shelf DE0-NANO FPGA development board, and a Cypress FX3 SuperSpeed Explorer USB 3.0 board.

**Note** Dont use USB storage or video devices on the same USB bus as the DdD, it will crash the capture!

[How To Aquire?](https://docs.google.com/document/d/1liOpdM6z51AwM5jGLoUak6h9aJ0eY0fQduE5k4TcleU/edit?usp=sharing) / [How to Fabricate & Flash?](https://docs.google.com/document/d/1k2bPPwHPoG7xXpS1NCYEe3w_jD_ts0yRCp-2aQ6QoKY/edit?usp=sharing) / [More Information](https://www.domesday86.com/?page_id=978)

## [CX Card & CXADC](https://github.com/oyvindln/vhs-decode/wiki/CX-Cards) (20-35USD)

Capture & Config uses simple command-line arguments and parameters [CXADC](https://github.com/happycube/cxadc-linux3)

The budget approach is using a video capture card based on a Conexant CX23880/1/2/3 PCI chipset. With a modified Linux driver, these cards can be forced to output RAW data that can be captured to file, instead of decoding video normally as they otherwise would.

While you can use any generic card with the correct chips, today we recommend the ‘‘New’’ Chinese variants that can be found on AliExpress that have integrated Asmedia or ITE 1x PCIE bridge chips allowing modern systems to use them, and consistent performance.

[Ware to Buy? & More Info](https://github.com/oyvindln/vhs-decode/wiki/CX-Cards)

Sadly however at stock without any modifications CX Cards proform slightly worse then a DomesdayDuplicator with about a 3db signal to noise difference, and its internal digital gain can affect captures drastically.

Currently the CX23883-39 based white variant cards have been consistently lower noise, these have also been easily upgraded to 40msps 8-bit with a drop-in crystal upgrade for use with formats like LaserDisc, but at stock with external amplification they are quite optimal for VHS & HiFi, but higher bandwidth formats like SVHS & ED Beta can benifit from crystal upgrades.


# Deployment of Capture Hardware


Please read [VCR Reports](https://github.com/oyvindln/vhs-decode/wiki/VCR-reports) / [The Tap List](https://github.com/oyvindln/vhs-decode/wiki/004-The-Tap-List) / [Hardware Installation Guide](https://github.com/oyvindln/vhs-decode/wiki/Hardware-Installation-Guide)

Information on various VCRs that have been documented alongside high resolution pictures of VCR's that have had RF taps installed, guidance on recommended cables/connectors & tools to use are also included.

The setup process for RF capture involves running a short cable internally from test point or amplifyer points that provide the unprocessed video/hifi signals to a BNC jack at back of a metal/plastic VCR chassis or threaded out a vent, this allows direct access to the FM RF signals conveniently & reliably, we call this a Tap Point or RF Tap, for some decks and camcorders however Dupont conectors and ribbon jigs can be used on Video8 & Hi8.

`VCR ==> Head Drum ==> Amplification & Tracking ==> FM RF Test/Signal Points ==> FM RF Capture ==> Software Decoding & Dropout Detection ==> Lossless TBC Files ==> Dropout Correction ==> Standard Audio/Video File Creation.`

<img src="https://github.com/harrypm/vhs-decode/assets/56382624/d98c031d-d927-4554-abe1-eb0611108ad9" width="" height="">




# Dependencies & Installation - Software


VHS-Decode, as with LD-Decode, has been developed and tested on machines running the latest versions of Ubuntu and Linux Mint.
Other distributions might have outdated (or even newer) versions of certain Python libraries or other dependencies, breaking compatibility.

There is a [Linux compatability doc](https://docs.google.com/document/d/132ycIMMNvdKvrNZSzbckXVEPQVLTnH_YX0Oh3lqtkkQ/edit) for various tested distributions of Linux.

Its fully working on WSL2 Ubuntu 20.04 (Windows Subsystem for Linux) however issues with larger captures i.g 180gb+ may require expanding the default [virtual disk size](https://docs.microsoft.com/en-us/windows/wsl/vhd-size)

Other dependencies include Python 3.5+, numpy, scipy, cython, numba, pandas, Qt5, Cmake, and FFmpeg.

Some useful free tools to note for post processing are
[StaxRip](https://github.com/staxrip/staxrip) & [Lossless Cut](https://github.com/mifi/lossless-cut) & of course [DaVinci Resolve](https://www.blackmagicdesign.com/uk/products/davinciresolve) - these give you basic editing to quickly handle uncompressed files across operating systems, and for Windows users an easy FFmpeg/AviSynth/Vapoursynth encoding and QTGMC de-interlacing experience, and full colour grading and post production ability.





# Usage


Note with WSL2 & Ubuntu, `./` in front of applications and scripts may be needed to run them.

Use `cd vhs-decode` to enter into the directory to run commands, `cd..` to go back a directory.

Use <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop the current process.

You dont actaully type `<` and `>` on your input & output files.


## Decoding RF Captures


Decode your captured tape to a .tbc by using:

    vhs-decode [arguments] <capture file> <output name>

Basic Usage Example:

    ./vhs-decode --debug --pal --threads 8 --tape_format VHS --cxadc CX-White-2022.10.25.u8 my-first-decode-2022.10.25

After decoding process your tapes VBI data with:

    ld-process-vbi <decoded tape name>.tbc

Use analyse tool to inspect decoded tape data:

    ld-analyse <decoded tape name>.tbc

(TBC are headerless you can open them at any time during decoding, preview is limited to what frame info has been fully written to the JSON file)

<img src="https://github.com/oyvindln/vhs-decode/wiki/assets/images/Post-Processing/ld-analyse-chroma-frame-107-2023-02-23-23-01-21.png"  width="600" height="">

## Compression and Decompression

For DomesDayDuplicator captures on Linux simply run:

`ld-compress <capture>`

For DomesDayDuplicator captures on Windows simply drag and drop on: 

`ld-compress.bat` or `ld-compress-nvidia-gpu.bat`

Your `.lds` file will be compressed to an FLAC OGG `.ldf` file.

For CXADC and other 8/16bit captures use the following:

[Copy Paste FLAC Compression Commands for CXADC](https://github.com/happycube/cxadc-linux3/wiki/FLAC-Compression-Guide#post-capture-flac-compression)

Editable flags are:

The `--bps` flag can be changed to `--bps=8` or `--bps=16` for 8 & 16 bit captures and `--ogg` is optional.

Change `<capture>` & `<output-name>` to your input & output file name.

Reduce size of captured CXADC data (by 40-60%):

    flac --best --sample-rate=28636 --sign=unsigned --channels=1 --endian=little --bps=8 --ogg -f <capture>.u8 <output-name>

Output will be `filename.ogg` so rename the end extension to `.vhs` / `.hifi` etc.

Decompress FLAC compressed captures:

    flac -d --force-raw-format --sign=unsigned --endian=little <capture>.vhs <capture>.u16


## Generating Colour Video Files (.TBC to Playable .MKV)

Some useful free tools to note for post processing are [StaxRip](https://github.com/staxrip/staxrip) & [Lossless Cut](https://github.com/mifi/lossless-cut) & of course [DaVinci Resolve](https://www.blackmagicdesign.com/uk/products/davinciresolve) 

These tools give you editing to quickly handle uncompressed files across operating systems, and for Windows users an easy FFmpeg/AviSynth/Vapoursynth encoding and QTGMC de-interlacing experience, and full colour grading and post production ability.

### [Read the full exporting guide here](https://github.com/oyvindln/vhs-decode/wiki/Video-Exporting-&-Gen-Chroma-Scripts)

<img src="https://github.com/oyvindln/vhs-decode/wiki/assets/images/Post-Processing/TV-PC-Levels.png" width="600" height="">


VHS-Decode produces two timebase corrected 16-bit `GREY16` headerless files separated into chroma/luma composite video signals in the `.tbc` format `filename.tbc` & `filename_chroma.tbc` respectively alongside `.json` and `.log` files with frame and decode information, usable with the LD-Decode family of tools ld-analyse, ld-process-vbi, ld-process-vits, ld-dropout-correct & ld-chroma-decoder etc 

The gen chroma scrips will use decoded .tbc files and generate standard video files - by default a lossless, interlaced top field first and high-bitrate (roughly 70-100 Mb/s) FFV1 codec video which, which although ideal for archival and further processing has only recently started to gain support in modern [NLEs](https://en.wikipedia.org/wiki/Non-linear_editing).

*gen_chroma_vid.sh automatically detects PAL/NTSC based on the .JSON, although legacy scripts still exist*

To generate .mkv files viewable in most media players, simply use the `gen_chroma_vid.sh` script below.

### Export your TBC files to a video file with the following basic command


    ./gen_chroma_vid.sh Input-TBC-Name


## Editing & Basic Online Usage


For editing due to lack of support of FFV1 and sharing online without [de-interlacing](https://github.com/oyvindln/vhs-decode/wiki/Deinterlacing) is not supported properly at all, as such the two commands are provided below to make suitable starting files for this use.

Both commands will automatically use the last file generated as the input.

For editors this transcodes an FFV1/V210 output to a "*near compliant*" interlaced ProRes HQ file:
    
    ffmpeg -hide_banner -i "$1.mkv" -vf setfield=tff -flags +ilme+ildct -c:v prores -profile:v 3 -vendor apl0 -bits_per_mb 8000 -quant_mat hq -mbs_per_slice 8 -pixel_format yuv422p10lep -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a s24le -vf setdar=4/3,setfield=tff "$1_ProResHQ.mov"
    
For basic online sharing you can use this command to convert the FFV1 output to a de-interlaced lossy upscaled MP4:
    
    ffmpeg -hide_banner -i "$1.mkv" -vf scale=in_color_matrix=bt601:out_color_matrix=bt709:1440x1080,bwdif=1:0:0 -c:v libx264 -preset veryslow -b:v 15M -maxrate 15M -bufsize 8M -pixel_format yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -aspect 4:3 -c:a libopus -b:a 192k -strict -2 -movflags +faststart -y "$1_1440x1080_lossy.mp4"

To just export the video with standard settings and the same input file name, the .tbc extention is not required.

## Time Control & Audio Muxing

Command Examples:

    ./gen_chroma_vid.sh -v -s <skip number of frames> -l <number of frames long> -i <.tbc filename without .tbc extension>

The `-a` option can embed an audio file, such as audio decoded via [HiFi Decode](https://github.com/VideoMem/ld-decode/tree/hifi-decode)

    ./gen_chroma_vid.sh -v -s <skip n frames> -l <n frames long> -a <capture>.flac -i <.tbc filename without .tbc extension>

So for example open terminal in the directory of target TBC/Metadata files and run

    ./gen_chroma_vid.sh -v -s <skip n frames> -l <number of frames long> -a <capture>.flac -i <.tbc filename without .tbc extension>


## VBI (Vertical Blanking Interval) Data Recovery


Software decoding provides the full signal frame, recovery software can be used to read and extract this information, however some information can be automatically extracted in the TBC file stage with `ld-processs-vbi` like VITC & Closed Captions. 

[VITC Timecode](https://github.com/oyvindln/vhs-decode/wiki/VITC-SMPTE-Timecode) (Standard SMPTE Timecode)

[CC EIA-608](https://github.com/oyvindln/vhs-decode/wiki/Closed-Captioning) (Closed Captioning)

[Teletext](https://github.com/oyvindln/vhs-decode/wiki/Teletext) (European Subtitles & Information Graphics)

[Tape-based Arcade Games!](https://vhs.thenvm.org/resources/)

[Ruxpin TV Teddy](https://github.com/oyvindln/vhs-decode/blob/vhs_decode/tools/ruxpin-decode/readme.pdf) (Extra audio in visable frame)

### Generate an video output with the top VBI area:

<img src="https://github.com/oyvindln/vhs-decode/wiki/assets/images/Post-Processing/Jennings-With-VBI.png" width="600" height="">

PAL

    ./gen_chroma_vid.sh --ffll 2 --lfll 308 --ffrl 2 --lfrl 620 <tbc-name>

NTSC

    ./gen_chroma_vid.sh --ffll 1 --lfll 259 --ffrl 2 --lfrl 525 <tbc-name>


## Terminal Arguments


VHS-Decode supports various arguments to change how captured tape recordings are processed. These vary slightly between formats like VHS & Umatic but the basic oprations remain the same.

The list below is a short list for common/daily usage but does not cover all the abilities and new or advanced command arguments possible so please read the [complete and upto-date command list](https://github.com/oyvindln/vhs-decode/wiki/Command-List) on the wiki as commands may change or be deprecated, so its always good to check this list for any updates.


## Sample Rate Comamnds

By default, this is set to 40 MHz (the sample rate used internally and by the Domesday Duplicator) at 16 bits.

The decoder is 8/16 bit agnostic so as long as sample rate is defined, it will decode it.

`-f`  Adjusts sampling frequency in integer units.

Example's `-f 280000hz` or `-f 28mhz` or `-f 8fsc`

`-tf` Sets Tape Format enter `VHS`, `SVHS`, `UMATIC`, `UMATIC_HI`, `BETAMAX`, `VIDEO8`, `HI8`, `TYPEC`, `EIAJ`, `VCR` (Default is VHS)


##  CXADC Specific Sample Rate Commands


`--cxadc`    28.6 MHz/8-bit  (8fsc)

`--cxadc3`   35.8 MHz/8-bit  (10fsc) (Not recommended for capture due to up-sampling)

`--10cxadc`  14.3 MHz/16-bit (4fsc)

`--10cxadc3` 17.9 MHz/16-bit (5fsc)


## Colour System Commands


Changes the colour or TV system to NTSC, PAL, PAL-M, NTSC-J, or [MESECAM](https://en.wikipedia.org/wiki/SECAM#MESECAM_(home_recording)) respectively.
Please note that, as of this writing, support for PAL-M is **experimental**.

`-n` = NTSC

`-p` = PAL

`--pm` = PAL-M

`--NTSCJ` = NTSC-J

`--MESECAM` = MESECAM


# [Time & Location Control](https://github.com/oyvindln/vhs-decode/wiki/Command-List#time--location-control)


These commands are used for jumping ahead in a file or for defining limits.
Useful to recover decoding after a crash, or for limiting process time by producing shorter samples.

`-s`  Jumps ahead to any given frame in the capture.

`--start_fileloc` Jumps ahead to any given *sample* in the capture.

`-l` Limits decode length to *n* frames.

`-t` Defines the number of processing threads to use during demodulation, decode cant use more then 6-8 threads per decode currently so using 8 threads is the practical limit as its mostly a single core task.

(note: upon crashing, vhs-decode automatically dumps the last known sample location in the terminal output)


## [Time Base Correction & Visuals Control](https://github.com/oyvindln/vhs-decode/wiki/Command-List#decode-tbc---time-base-correction-control)


`--debug` sets logger verbosity level to *debug*. Useful for debugging and better log information. (Recommended to enable for archival.)

`--ct` enables a *chroma trap*, a filter intended to reduce chroma interference on the main luma signal. Use if seeing banding or checkerboarding on the main luma .tbc in ld-analyse.

`--recheck_phase` re-check chroma phase on every field, fixes most colour issues. (No effect on U-matic.)

`--sl` defines the output *sharpness level*, as an integer from 0-100, the default being 0. Higher values are better suited for plain, flat images i.e. cartoons and animated material, as strong ghosting can occur. (Akin to cranking up the sharpness on any regular TV set.)

`--dp demodblock` displays Raw Demodulated Frequency Spectrum Graphs, makes a pop-up window per each thread so -t 32 will give you 32 GUI windows etc


## Input file formats:


**Note** The decoders can be RAW uncompressed data or FLAC compressed data. 

**Note** .RAW will need to be renamed to s16/u16 

`.ldf`/`.lds` (40msps Domesday Duplicator FLAC-compressed and uncompressed data).

`.r8`/`.u8`   (CXADC 8-bit raw data).

`.r16`/`.u16` (CXADC 16-bit raw data).

.flac/.cvbs/.vhs/.svhs/.betacam/.betamax/.video8/.hi8 (FLAC-compressed captures, can be either 8-bit or 16-bit).


## Output file formats:


Unlike CVBS-Decode & LD-Decode, VHS-Decode does not output its timebase-corrected frames as a single .tbc file for colour-under formats.

Both the luminance and chrominance channels are separate data files, essentially a digital "S-Video", additionally useful for troubleshooting. Descriptor/log files are generated so you end up with 4 files with the following naming:

`filename.tbc`        - Luminance (Y) Image Data (Combined file CVBS)

`filename_chroma.tbc` - Chrominance (C) Image Data (QAM Modulated)

`filename.tbc.json`   - Frame Descriptor Table (Resolution/Dropouts/SNR/Frames/VBI Timecode)

`filename.log`        - Timecode Indexed Action/Output Log


# Join us!


[Discord](https://discord.gg/pVVrrxd)

[Reddit](https://www.reddit.com/r/vhsdecode/)

[VideoHelp Forum](https://forum.videohelp.com/threads/394168-Current-status-of-ld-decode-vhs-decode-(true-backup-of-RF-signals)#post2558660)

[Facebook](https://www.facebook.com/groups/2070493199906024)


# More Documentation


[VHS-Decode Wiki](https://github.com/oyvindln/vhs-decode/wiki)

[Google Doc Documentation](https://docs.google.com/document/d/1ZzR3gbW6iSVSNP0qoDIS0ExeRecKehlTQ0EJyx2g568/edit?usp=sharing)

## *If in doubt - feel free to read the docs/wiki again, if its not there then ask!*

For future documentation changes & sample submissions, speak with [Harry Munday](https://github.com/harrypm) (harry@opcomedia.com) or on Discord (therealharrypm)
