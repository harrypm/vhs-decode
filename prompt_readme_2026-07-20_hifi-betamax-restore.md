# Prompt session log — 2026-07-20 — hifi Betamax/Betacam placeholder restore

Working dir: `/Users/harry/vhs-decode` (branch `vhs_decode`, HEAD `5d12c9e7`)

## User inputs (this session)
1. "my hifi-decode changes for the Betamax/Betacam decoding were modifyed for no reason during my last session of fixing" (with attached shell commands: `cd ..`, `cd vhs-decode`, `git checkout vhs_decode`).
2. "The place holders were removed..."
3. "They were removed from the GUI without me asking..."
4. "ffs just add back the lines"

## Investigation (commands run + key findings)
- `git --no-pager status` → clean tree, on `vhs_decode` (HEAD `5d12c9e7`).
- `git --no-pager log --oneline -30` → commit `122a2825` "feat(launcher/hifi): ... Betamax/Betacam placeholders" added the placeholders; later `5d12c9e7` "fixes UX on macos" removed them.
- `git --no-pager reflog -40` → confirmed `5d12c9e7` is current HEAD; a `reset: moving to harrypm/vhs_decode` appears at HEAD@{3}.
- `git --no-pager show --stat 122a2825` → original placeholder commit touched `decode_launcher.py` (+157) and `hifi/HifiUi.py` (+83).
- `git --no-pager diff 122a2825 5d12c9e7 -- vhsdecode/hifi/HifiUi.py` → showed net removal of Betamax/Betacam placeholder handling (plus unrelated afe deviation rename from intermediate commits).
- `git --no-pager show 5d12c9e7 -- vhsdecode/hifi/HifiUi.py` → **the exact single commit** that removed: `format_combo` Betamax/Betacam items + tooltip, the three `("VHS","Betamax","Betacam")` format mappings, `PLACEHOLDER_FORMATS`, `_warn_if_placeholder_format`, `_is_placeholder_format_selected`, and the Play/Preview warning guards. It ALSO removed an unrelated `input_format_override` round-trip (added earlier by `904a21d2`) — left untouched per user scope.
- `git --no-pager log -p -S 'PLACEHOLDER_FORMATS'` → confirmed `5d12c9e7` is the commit that deleted `PLACEHOLDER_FORMATS`.
- `grep` for Betamax/Betacam across `vhsdecode/` → real Betamax decode logic exists in `vhsdecode/format_defs/betamax.py`, `field.py`, `chroma.py`, `debug_plot.py`; launcher `decode_launcher.py` still routes Betamax/Betacam to hifi.

## Edits made
File: `vhsdecode/hifi/HifiUi.py` — restored exactly the lines removed by `5d12c9e7` (Betamax/Betacam placeholders only; macOS UX changes and `input_format_override` change left as-is):
1. Line ~266 `ui_parameters_to_decode_options`: `"format": "vhs" if values.format in ("VHS","Betamax","Betacam") else "8mm"`.
2. Line ~654 `build_format_options_section`: `format_combo.addItems(["VHS","Video8/Hi8","Betamax","Betacam"])` + restored tooltip.
3. Line ~1238 `update_afe_values`: `"vhs" if format in ("VHS","Betamax","Betacam") else "8mm"`.
4. Line ~1251 `update_deemphasis_expander_values`: `if format in ("VHS","Betamax","Betacam"):`.
5. Lines ~1288-1313 `on_format_change` + restored `PLACEHOLDER_FORMATS`, `_warn_if_placeholder_format`, `_is_placeholder_format_selected`.
6. Lines ~1370-1375 `on_play_clicked`: restored placeholder warning guard.
7. Lines ~1384-1389 `on_preview_clicked`: restored placeholder warning guard.

## Verification (commands run + results)
- `python3 -m py_compile vhsdecode/hifi/HifiUi.py` → `PY_COMPILE_OK` (no syntax errors).
- `grep` Betamax/Betacam/PLACEHOLDER_FORMATS in `HifiUi.py` → present at lines 266, 654-662, 1238, 1251, 1295, 1297, 1299, 1300, 1312, 1313, 1372, 1373, 1386, 1387 (plus pre-existing auto-detect at 1817/1827/1829).
- `git --no-pager diff --stat -- vhsdecode/hifi/HifiUi.py` → `1 file changed, 39 insertions(+), 6 deletions(-)`, isolated to `HifiUi.py`.

## NOT yet verified (pending real-world confirmation)
- GUI has NOT been launched. Per GUI-confirmation rule, user must run `hifi-decode` GUI and confirm:
  - Format dropdown shows VHS / Video8/Hi8 / Betamax / Betacam.
  - Selecting Betamax or Betacam pops the "Place Holder - Format yet to be implemented" QMessageBox.
  - Play/Preview with Betamax/Betacam selected also pops the warning.
  - Tooltip on the Format combo shows the placeholder explanation.

## Restore point
- Pre-edit HEAD: `5d12c9e7` (clean). To revert this restoration: `git checkout -- vhsdecode/hifi/HifiUi.py`.
- No zip/restore-point archive created yet (only required once user confirms the fix is fully working).
