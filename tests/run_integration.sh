#!/bin/bash
set -euo pipefail

# Enable hash regeneration with:
#   REGENERATE_HASHES=1 ./script.sh
# or:
#   ./script.sh --regenerate-hashes
REGENERATE_HASHES="${REGENERATE_HASHES:-0}"

if [[ "${1:-}" == "--regenerate-hashes" ]]; then
    REGENERATE_HASHES=1
    shift
fi

# Global flags applied to every vhs-decode invocation.
GLOBAL_FLAGS=(--no_resample --threads 3)

TEST_ROOT="${GITHUB_WORKSPACE:-$(pwd)}/tests"
TEST_DATA_INPUT="$TEST_ROOT/data"
TEST_DATA_OUTPUT=$(mktemp -d)

EXPECTED_HASHES="$TEST_ROOT/integration/hashes"
CALC_HASH="$TEST_ROOT/integration/calc_hash.sh"
CHECK_HASH="$TEST_ROOT/integration/check_hash.sh"

pass_count=0
passes=""
fail_count=0
failures=""

hash_pass_count=0
hash_passes=""
hash_fail_count=0
hash_failures=""

# ── Registry helpers ─────────────────────────────────────────────────────────

declare -A SYS TF FREQ FLAGS
BASIC_TESTS=()

# Register an input sample for basic testing.
#   input <basename> <system> <tf> <freq> [optional_flags...]
input() {
    local name="$1" system="$2" tf="$3" freq="$4"
    shift 4
    SYS[$name]="$system"
    TF[$name]="$tf"
    FREQ[$name]="$freq"
    FLAGS[$name]="$*"
    BASIC_TESTS+=("$name")
}

declare -A MUT_BASE MUT_FLAGS
MUTATION_TESTS=()

# Register a mutation test on an existing input.
#   mutation <output_basename> <base_input> <extra_flags...>
mutation() {
    local name="$1" base="$2"
    shift 2
    MUT_BASE[$name]="$base"
    MUT_FLAGS[$name]="$*"
    MUTATION_TESTS+=("$name")
}

# ── Execution engine ─────────────────────────────────────────────────────────

# Build and run a vhs-decode command.
#   run_decode <input_basename> <output_basename> [extra_flags...]
#
# Flag order mirrors the originals:
#   --system  [--tf]  [per-input flags]  -f  [global]  [mutation flags]  input.flac  output
run_decode() {
    local test_name="$1" input_name="$2" output_name="$3"
    shift 3

    local -a cmd=(vhs-decode "${GLOBAL_FLAGS[@]}" --system "${SYS[$input_name]}" --tf "${TF[$input_name]}" -f "${FREQ[$input_name]}")

    if [[ -n "${FLAGS[$input_name]}" ]]; then
        local -a input_flags
        read -ra input_flags <<< "${FLAGS[$input_name]}"
        cmd+=("${input_flags[@]}")
    fi

    if [[ $# -gt 0 ]]; then
        cmd+=("$@")
    fi

    cmd+=("$TEST_DATA_INPUT/${input_name}.flac" "$TEST_DATA_OUTPUT/$output_name")

    echo "${cmd[*]}"
    if "${cmd[@]}"; then
        (( ++pass_count ))
        passes+="${test_name}"$'\n'
    else
        echo "FAILED: ${test_name}" >&2
        (( ++fail_count ))
        failures+="${test_name}"$'\n'
    fi
}

assert_decode_output() {
    local test_name="$1" input_name="$2" result=0

    if (( REGENERATE_HASHES )); then
        echo "Regenerating hashes for: $input_name"
        "$CALC_HASH" "$input_name" "$TEST_DATA_OUTPUT" "$EXPECTED_HASHES"
    fi

    $CHECK_HASH "$input_name" "$TEST_DATA_OUTPUT" "$EXPECTED_HASHES" || result=$?

    if (( result == 0)); then
        (( ++hash_pass_count ))
        hash_passes+="${test_name}"$'\n'
    else
        echo "FAILED: ${test_name}" >&2
        (( ++hash_fail_count ))
        hash_failures+="${test_name}"$'\n'
    fi
}

# ── Basic test inputs ────────────────────────────────────────────────────────
#   input <basename> <system> <tf> <freq> [flags...]

input betamax_405           405           BETAMAX       40.0
input betamax_pal           PAL           BETAMAX       20.0
input eiaj_pal              PAL           EIAJ          28.636
input hi8_ntsc              NTSC          HI8           28.636
input hi8_pal               PAL           HI8           40.0
input quadruplex_819        819           QUADRUPLEX    40.0
input quadruplex_pal        PAL           QUADRUPLEX    40.0
input superbeta_ntsc_lp     NTSC          SUPERBETA     40.0  --ts LP
input svhs_et_ntsc          NTSC          SVHS_ET       40.0
input svhs_et_pal           PAL           SVHS_ET       40.0
input svhs_pal              PAL           SVHS          40.0
input typeb_pal             PAL           TYPEB         40.0
input typec_ntsc            NTSC          TYPEC         40.0
input typec_pal             PAL           TYPEC         40.0
input umatic_ntsc           NTSC          UMATIC        40.0
input umatic_pal            PAL           UMATIC        17.898
input vcr_pal               PAL           VCR           40.0
input vhs_mesecam           MESECAM       VHS           17.898
input vhs_nlinha            NLINHA        VHS           40.0
input vhs_ntsc              NTSC          VHS           17.9
input vhs_ntsc_lp           NTSC          VHS           20.0  --ts LP
input vhs_pal               PAL           VHS           40.0  --fallback_vsync --relaxed_line0
input vhs_palm              PALM          VHS           40.0  --ts SLP
input video2000_pal         PAL           VIDEO2000     28.636
input video8_ntsc           NTSC          VIDEO8        40.0
input video8_pal            PAL           VIDEO8        40.0

# ── Mutation tests ───────────────────────────────────────────────────────────
#   mutation <output_basename> <base_input> <extra_flags...>

mutation  _cafc                       "vhs_ntsc"        --cafc
mutation  _cafc_notch                 "vhs_ntsc"        --cafc --notch 3.58
mutation  _cafc_umatic                "umatic_pal"      --cafc
mutation  _cafc_video8                "video8_pal"      --cafc
mutation  _chroma_trap                "vhs_ntsc"        --ct
mutation  _clamp                      "vhs_pal"         --clamp
mutation  _detect_chroma_track_phase  "vhs_ntsc"        --dctp
mutation  _dod_threshold_abs          "vhs_ntsc"        --dod_t_abs 5000
mutation  _export_raw_tbc             "vhs_pal"         --export_raw_tbc
mutation  _fallback_vsync_ntsc        "svhs_et_ntsc"    --fallback_vsync
mutation  _fm_audio_notch             "vhs_ntsc"        --fm_audio_notch 10
mutation  _ire0_adjust                "vhs_ntsc"        --ire0_adjust
mutation  _nld                        "vhs_ntsc"        --nld
mutation  _notch_ntsc                 "vhs_ntsc"        --notch 3.58
mutation  _notch_pal                  "vhs_pal"         --notch 4.43
mutation  _saved_levels               "svhs_et_ntsc"    --use_saved_levels
mutation  _sharpness                  "vhs_ntsc"        --sl 50
mutation  _skip_hsync_refine          "vhs_ntsc"        --skip_hsync_refine
mutation  _track_phase1               "vhs_ntsc"        --track_phase 1
mutation  _wow_cubic                  "vhs_ntsc"        --wow_interpolation_method cubic
mutation  _wow_quadratic              "vhs_ntsc"        --wow_interpolation_method quadratic
mutation  _wow_smooth500              "vhs_ntsc"        --wow_level_adjust_smoothing 500
mutation  _y_comb                     "vhs_ntsc"        --y_comb 1.5

# ── Run ──────────────────────────────────────────────────────────────────────

echo "=== Basic tests ==="
echo ""

for _name in "${BASIC_TESTS[@]}"; do
    TEST_NAME="Basic Test, $_name"

    echo "::group::$TEST_NAME"
    run_decode "$TEST_NAME" "$_name" "$_name"
    # TODO: Figure out a way to deterministically compare the TBC files
    #       Decodes are slightly different depending on the python version / system architecture
    # assert_decode_output "$TEST_NAME" "$_name" "$_name"
    echo "::endgroup::"
done

echo ""
echo "=== Mutation tests ==="
echo ""

for _name in "${MUTATION_TESTS[@]}"; do
    read -ra _extra <<< "${MUT_FLAGS[$_name]}"

    TEST_NAME="Mutation Test, $_name ${MUT_BASE[$_name]}"

    echo "::group::$TEST_NAME"
    run_decode "$TEST_NAME" "${MUT_BASE[$_name]}" "$_name" "${_extra[@]}"
    # TODO: Figure out a way to deterministically compare the TBC files
    #       Decodes are slightly different depending on the python version / system architecture
    echo "::endgroup::"
done

# ── Summary ──────────────────────────────────────────────────────────────────

total=$(( pass_count + fail_count ))
echo ""
echo "=== Results: ${pass_count}/${total} passed, ${fail_count} failed ==="

echo ""
echo "=== Passed Decode ==="
echo "${passes:-None}"

echo ""
echo "=== Passed Hash ==="
echo "${hash_passes:-None}"

echo ""
echo "=== Failed Decode ==="
echo "${failures:-None}"

echo ""
echo "=== Failed Hash ==="
echo "${hash_failures:-None}"

exit $(( fail_count > 0 ? 1 : 0 ))
