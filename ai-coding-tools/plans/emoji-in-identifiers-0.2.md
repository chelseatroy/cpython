# Plan: Emoji in Python Identifiers — Range Selection (v0.2)

## Goal

Define the exact set of Unicode ranges whose characters should be valid in Python identifiers (as both start and continuation characters), beyond what XID_Start/XID_Continue already permit.

## Selected Ranges

### BMP Symbol Blocks

| Block | Range | Codepoints | Notes |
|-------|-------|------------|-------|
| Miscellaneous Technical (8 chars only) | See sub-range below | 8 | Cherry-picked emoji-like characters only. See Sub-Range Selections. |
| Geometric Shapes | U+25A0..U+25FF | 96 | ■ □ ▲ △ ● ○ ◆ etc. Text-style shapes that render consistently across platforms (unlike emoji). Included deliberately for that stability. |
| Miscellaneous Symbols | U+2600..U+26FF | 256 | ★ ♥ ☀ ⚡ ♠ ♣ etc. Already in v0.1 implementation. |
| Dingbats | U+2700..U+27BF | 192 | ✂ ✓ ✔ ✈ ❤ ✨ etc. Already in v0.1 implementation. |
| Miscellaneous Symbols and Arrows | U+2B00..U+2BFF | 256 | ⭐ ⬆ ⬇ ⭕ etc. New addition (not in v0.1). |

### SMP Emoji Blocks

| Block | Range | Codepoints | Notes |
|-------|-------|------------|-------|
| Miscellaneous Symbols and Pictographs | U+1F300..U+1F5FF | 768 | 🌀🎉🔥 etc. Includes skin tone modifiers (U+1F3FB–U+1F3FF). Already in v0.1. |
| Emoticons | U+1F600..U+1F64F | 80 | 😀😎🙏 etc. Already in v0.1. |
| Transport and Map Symbols | U+1F680..U+1F6FF | 128 | 🚀🛸🚗 etc. Already in v0.1. |
| Geometric Shapes Extended | U+1F780..U+1F7FF | 128 | 🟢🟠🟡🟣🟥 etc. Already in v0.1. |
| Supplemental Symbols and Pictographs | U+1F900..U+1F9FF | 256 | 🤖🧠🤝 etc. Already in v0.1. |
| Chess Symbols | U+1FA00..U+1FA6F | 112 | New addition (v0.1 covered this range but unintentionally as part of a wider U+1FA00–U+1FAFF span). |
| Symbols and Pictographs Extended-A | U+1FA70..U+1FAFF | 144 | 🪐🫠 etc. Already in v0.1 (as part of wider span). |

### Sub-Range Selections

| Name | Range | Codepoints | Notes |
|------|-------|------------|-------|
| Regional Indicators | U+1F1E6..U+1F1FF | 26 | 🇦–🇿 (flag building blocks). Sub-range of Enclosed Alphanumeric Supplement. Only these 26 codepoints, not the full block. Already in v0.1. |
| Miscellaneous Technical (cherry-picked) | 8 individual codepoints | 8 | Emoji-like characters only, excluding the ~248 technical diagram symbols. Full block rejected as too mixed. |

**Miscellaneous Technical — individual codepoints:**

| Char | Codepoint | Name |
|------|-----------|------|
| ⌚ | U+231A | WATCH |
| ⌛ | U+231B | HOURGLASS |
| ⏩ | U+23E9 | BLACK RIGHT-POINTING DOUBLE TRIANGLE |
| ⏪ | U+23EA | BLACK LEFT-POINTING DOUBLE TRIANGLE |
| ⏫ | U+23EB | BLACK UP-POINTING DOUBLE TRIANGLE |
| ⏬ | U+23EC | BLACK DOWN-POINTING DOUBLE TRIANGLE |
| ⏰ | U+23F0 | ALARM CLOCK |
| ⏳ | U+23F3 | HOURGLASS WITH FLOWING SAND |

---

## Ranges Considered and Excluded

### Already valid via XID (no action needed)

These script blocks were initially selected but removed because their letters are already valid Python identifier characters through the Unicode XID_Start/XID_Continue properties. Selecting entire blocks would only add their punctuation and format characters, which is harmful.

| Block | Range | Why excluded |
|-------|-------|-------------|
| Latin Extended-A | U+0100..U+017F | Letters already in XID. |
| Latin Extended-B | U+0180..U+024F | Letters already in XID. |
| IPA Extensions | U+0250..U+02AF | Letters already in XID. |
| Greek and Coptic | U+0370..U+03FF | Letters already in XID. Whole-block inclusion would add U+037E (Greek question mark, identical to ASCII `;`). |
| Cyrillic Supplement | U+0500..U+052F | Letters already in XID. |
| Armenian | U+0530..U+058F | Letters already in XID. Whole-block inclusion would add punctuation (full stop, hyphen). |
| Hebrew | U+0590..U+05FF | Letters already in XID. Whole-block inclusion would add punctuation (maqaf, paseq, geresh, gershayim). |
| Arabic | U+0600..U+06FF | Letters already in XID. Whole-block inclusion would add **invisible format characters** (U+0600–U+0605, U+061C, U+06DD) and punctuation. |
| Syriac | U+0700..U+074F | Letters already in XID. Whole-block inclusion would add **invisible format character** (U+070F) and punctuation. |
| Arabic Supplement | U+0750..U+077F | Letters already in XID. |

### Excluded for safety

| Block | Range | Why excluded |
|-------|-------|-------------|
| Basic Latin | U+0000..U+007F | Contains all Python operators (`+` `-` `*` `/` `=` etc.), delimiters (`(` `)` `[` `]` `{` `}` `:` `;` etc.), whitespace, and control characters. Would break the language. |
| Latin-1 Supplement | U+0080..U+00FF | Contains C1 control characters (U+0080–U+009F), non-breaking space (U+00A0, visually identical to regular space), and `×` (U+00D7, confusable with letter `x`). |
| General Punctuation | U+2000..U+206F | Contains various-width spaces (U+2000–U+200A), zero-width space (U+200B), bidi overrides (U+200E–U+200F, U+202A–U+202E), smart quotes (U+2018–U+201F), line/paragraph separators (U+2028–U+2029). Security minefield. |

### Excluded — SMP gaps (intentional)

| Block | Range | Why excluded |
|-------|-------|-------------|
| Ornamental Dingbats | U+1F650..U+1F67F | Decorative variants, not commonly used emoji. |
| Alchemical Symbols | U+1F700..U+1F77F | Alchemical/chemical notation, not emoji. |
| Supplemental Arrows-C | U+1F800..U+1F8FF | Arrows, not emoji. |

---

## Design Decisions

### Decided

2. **Geometric Shapes (U+25A0..U+25FF): INCLUDE.** These are text-style shapes (■ ● ▲) rather than colorful emoji, but that's a feature: they render consistently across platforms, fonts, and terminals, avoiding the visual ambiguity problem that plagues emoji. They're useful as identifiers precisely because of that stability.

3. **Unassigned codepoints within selected blocks: EXCLUDE.** Block-based ranges risk automatically accepting whatever Unicode assigns to currently-empty slots in future versions. The implementation should check only currently-assigned codepoints, not entire block ranges. This requires maintaining an explicit list rather than simple range checks, but avoids silently accepting unknown future characters as valid identifiers.

3. **Miscellaneous Technical (U+2300..U+23FF): CHERRY-PICK 8 characters.** The full block is too mixed — it contains useful emoji-like characters alongside obscure technical diagram symbols. Rather than include or exclude the whole block, we enumerate exactly the 8 emoji-like characters we want (⌚⌛⏩⏪⏫⏬⏰⏳) and reject the rest.

---

## Changes from v0.1 Implementation

| Change | Detail |
|--------|--------|
| **Added** | Geometric Shapes (U+25A0..U+25FF) |
| **Added** | Miscellaneous Symbols and Arrows (U+2B00..U+2BFF) |
| **Added** | Chess Symbols (U+1FA00..U+1FA6F) as explicit inclusion |
| **Tightened** | Extended-A from U+1FA00..U+1FAFF to two explicit blocks: Chess Symbols (U+1FA00..U+1FA6F) + Extended-A (U+1FA70..U+1FAFF) |
| **Tightened** | Implementation must skip unassigned codepoints within selected blocks, not accept entire ranges blindly. This changes the implementation approach from simple range checks to assigned-codepoint-only checks. |
| **Added** | Miscellaneous Technical — 8 cherry-picked emoji-like characters (not the full block) |
| **Retained** | All other v0.1 emoji ranges |
| **Retained** | Regional Indicators (U+1F1E6..U+1F1FF) |

---

## Implementation Method

Tests were written first and committed while failing (103 tests total, including v0.1 tests and new v0.2 tests). Two implementation approaches were then built in separate git worktrees so they could be compared side by side.

### Test Suite (committed before implementation)

- **V02NewRangeTests**: Tests for Geometric Shapes, Misc Symbols and Arrows, Chess Symbols, 8 cherry-picked Misc Technical characters, boundary tests, and negative tests for non-cherry-picked Misc Technical characters.
- **V02UnassignedCodepointTests**: Uses `unicodedata.category()` to find unassigned codepoints (category `Cn`) within each block at runtime. Skips gracefully if a block is fully assigned, making tests resilient to future Unicode updates.
- **V02FunctionalTests**: `exec()`-based tests that verify new ranges work in actual Python code alongside v0.1 ranges.

Boundary tests use last *assigned* codepoints rather than block-end codepoints (e.g. U+1F7F0 instead of U+1F7FF, U+1FA6D instead of U+1FA6F) since block-end codepoints may be unassigned.

### Approach A: Precise Sub-Ranges

**Branch:** `emoji-v02-approach-a` (worktree: `cpython-v02-approach-a`)

Splits blocks that contain unassigned gaps into precise assigned-only sub-ranges within `_PyUnicode_IsEmoji()`. The function itself only returns 1 for assigned codepoints, so no other files need changes.

**Files changed:** 2 (`pycore_unicodeobject.h`, `test_emoji_identifiers.py`)

Sub-range splits required:
- Misc Symbols and Arrows: 3 sub-ranges (gaps at U+2B74..U+2B75, U+2B96)
- Transport and Map Symbols: 3 sub-ranges (gaps at U+1F6D8..U+1F6DB, U+1F6ED..U+1F6EF)
- Geometric Shapes Extended: 3 sub-ranges (gaps at U+1F7DA..U+1F7DF, U+1F7EC..U+1F7EF)
- Symbols and Pictographs Extended-A: 8 sub-ranges (7 gaps)

Fully assigned blocks kept as single ranges: Geometric Shapes, Misc Symbols+Dingbats, Regional Indicators, Misc Pictographs, Emoticons, Supplemental Symbols.

### Approach B: Broad Ranges + PRINTABLE_MASK Filter

**Branch:** `emoji-v02-approach-b` (worktree: `cpython-v02-approach-b`)

Keeps broad block-level ranges in `_PyUnicode_IsEmoji()` but adds a second check: the codepoint must also have `PRINTABLE_MASK` set in CPython's Unicode type database. All assigned Symbol (So) characters have this flag; unassigned (Cn) characters do not. This filter is applied in three places:
- `_PyUnicode_IsXidStart()` in `unicodectype.c`
- `_PyUnicode_IsXidContinue()` in `unicodectype.c`
- `_PyUnicode_ScanIdentifier()` in `unicodeobject.c` (which calls `_PyUnicode_IsEmoji()` directly, bypassing `IsXidStart`/`IsXidContinue`)

**Files changed:** 4 (`pycore_unicodeobject.h`, `unicodectype.c`, `unicodeobject.c`, `test_emoji_identifiers.py`)

---

## Results Comparison

| | Approach A (precise sub-ranges) | Approach B (broad ranges + PRINTABLE_MASK) |
|---|---|---|
| **Test results** | 103 pass, 6 skip | 103 pass, 6 skip |
| **Files changed** | 2 | 4 |
| **Lines changed** | +137 / -36 | +98 / -39 |
| **#define constants** | 52 | 32 |
| **Range checks in IsEmoji** | ~27 | ~16 |
| **Changes to unicodectype.c** | None | PRINTABLE_MASK filter in IsXidStart/IsXidContinue |
| **Changes to unicodeobject.c** | None | IsPrintable check in ScanIdentifier |

### Tradeoffs

**Approach A** keeps all unassigned-filtering logic in one place (`_PyUnicode_IsEmoji` itself), so `unicodectype.c` and `unicodeobject.c` don't need changes. It has more `#define` constants and range checks, and Unicode version updates that assign new codepoints in gaps require updating the sub-ranges — but this is desirable, since it forces a deliberate review of whether each new character should be valid in identifiers.

**Approach B** has fewer constants and range checks, and automatically picks up newly assigned codepoints when CPython's Unicode database is updated (since they gain `PRINTABLE_MASK`). But this automatic inclusion is a risk: future assignments could include characters unsuitable for identifiers. The filtering logic is also spread across 3 files — the "is emoji" check is necessary but not sufficient, requiring a second "is assigned" check at each call site.

---

## Code Quality Review Comparison

Both approaches were reviewed across four dimensions: naming, comments, cohesion, and performance. Reviews were conducted by specialized agents examining all three changed source files (`pycore_unicodeobject.h`, `unicodectype.c`, `unicodeobject.c`).

### Naming

| | Approach A | Approach B |
|---|---|---|
| **Constant clarity** | Many abbreviated names (`EMOJI_MSA_SUB1_START`, `EMOJI_GEO_EXT_SUB*`, `EMOJI_EXT_A_SUB*`) require comments to decode | Fewer, more self-documenting names (`EMOJI_TRANSPORT_START`, `EMOJI_GEOMETRIC_EXT_START`, `EMOJI_EXTENDED_A_START`) |
| **Constant count** | 46+ `#define` constants with inconsistent abbreviation depth | ~22 `#define` constants, easier to scan |

**Shared issues:** `prev_was_emoji` is misleading at initialization (captures *current* char's status). `EMOJI_MISC_TECH_FF` and `EMOJI_MISC_TECH_REW` are unclear abbreviations in both. ZWJ (`0x200D`) and VS16 (`0xFE0F`) appear as magic numbers without named constants in both.

**Winner: Approach B** — fewer, clearer constant names.

### Comments

| | Approach A | Approach B |
|---|---|---|
| **Header comments** | Verbose gap documentation (e.g., "Gaps: U+2B74..U+2B75, U+2B96") — informative but risks going stale | Shorter section headers, some superfluous ("BMP symbol blocks", "SMP emoji blocks") |
| **API contract docs** | `_PyUnicode_IsEmoji` docstring is accurate but doesn't warn callers about obligations | `_PyUnicode_IsEmoji` docstring explicitly warns callers must verify assignment. `unicodectype.c` docstrings explain `PRINTABLE_MASK` rationale |

**Shared issues:** "Constrained ZWJ: only allow ZWJ between emoji" is slightly misleading in both (ZWJ is also allowed after non-emoji for Indic scripts). "VS16 does not change emoji state" is superfluous in both.

**Winner: Approach B** — better API contract documentation, though Approach A's gap-documenting comments are valuable context.

### Cohesion

| | Approach A | Approach B |
|---|---|---|
| **Encapsulation** | `_PyUnicode_IsEmoji` alone is the complete answer — no secondary check needed. Single point of truth for "is this a valid emoji identifier character?" | "Is this a valid emoji?" is scattered across 4 call sites repeating `_PyUnicode_IsEmoji(ch) && (PRINTABLE_MASK or IsPrintable)`. Two files use different-but-equivalent mechanisms. |
| **Future-proofing** | Sub-ranges must be manually updated when Unicode assigns new codepoints in gaps — this is deliberate, since newly assigned characters should be reviewed before being accepted as identifier characters | Newly assigned codepoints automatically become valid (they gain `PRINTABLE_MASK`) — this is a risk, since future assignments could include characters unsuitable for identifiers |

**Shared issues:** ZWJ/VS16 magic numbers should be named constants in the header. The `extern` declarations of `_PyUnicode_IsXidStart`/`_PyUnicode_IsXidContinue` in the header don't mention their emoji extension.

**Winner: Approach A** — single source of truth for encapsulation, and manual control over which codepoints are accepted is a safety feature, not a burden. Approach B's automatic inclusion of newly assigned codepoints is a liability: future Unicode assignments within these blocks could include characters unsuitable for identifiers, and they'd silently become valid without any review.

### Performance

| | Approach A | Approach B |
|---|---|---|
| **`_PyUnicode_IsEmoji` cost** | ~22 range comparisons worst-case | ~12 range comparisons worst-case (fewer, broader ranges) |
| **Additional per-char overhead** | None beyond `_PyUnicode_IsEmoji` | `_PyUnicode_IsPrintable` adds a `gettyperecord` table lookup (2 memory accesses) |
| **Double-eval issue** | Present: `_PyUnicode_IsEmoji` called in `ScanIdentifier` AND inside `IsXidStart`/`IsXidContinue` | Same issue, plus the additional `gettyperecord` double lookup |
| **Total cost per non-emoji, non-ASCII char** | ~22 comparisons + 1 table lookup | ~24 comparisons + 2 table lookups |

**Shared issues:** Both lack an ASCII fast-path before calling `_PyUnicode_IsEmoji` (it runs for every character including ASCII). Both could benefit from an outer range guard at the top of `_PyUnicode_IsEmoji` to reject characters below `0x231A` in a single comparison. The double-eval of `_PyUnicode_IsEmoji` (in `ScanIdentifier` and again inside `IsXidStart`/`IsXidContinue`) was already fixed on the main branch in commit `4200a3b9611` but neither approach variant has this fix.

**Winner: Approach A** — fewer total operations per character in the hot path.

### Summary Scorecard

| Dimension | Approach A | Approach B |
|-----------|-----------|-----------|
| **Naming** | Fair | Good |
| **Comments** | Good | Good+ |
| **Cohesion** | Good | Fair |
| **Performance** | Good | Fair |
| **Maintainability** | Good | Fair |

### Recommendation: Approach A (Precise Sub-Ranges)

Approach A is the better fit. The characters valid in Python identifiers should be manually specified, not automatically derived from Unicode metadata. Automatic inclusion of newly assigned codepoints (Approach B's key selling point) is actually a liability — there's no guarantee that future assignments within these blocks will be appropriate as identifier characters, and silently accepting them without review is unsafe. Approach A's precise sub-ranges require a manual update when Unicode assigns new codepoints to gaps, but that's a feature: it forces a deliberate decision about whether each new character belongs in identifiers.

Approach A also wins on cohesion (single source of truth in `_PyUnicode_IsEmoji`) and performance (fewer total operations per character). Its main weakness is naming — the many `#define` constants need clearer, more consistent names. Adopt Approach B's naming conventions (fewer abbreviations, more self-documenting) for the constants.

Additionally: the double-eval performance issue should be addressed by back-porting the fix from commit `4200a3b9611`, and both approaches should add named constants for ZWJ and VS16.

---

## Refactoring Plan for Approach A

The following changes address the review findings above. They are ordered from simplest to most complex — items 1–7 are cosmetic (names, comments, documentation) and items 8–10 change code paths for performance (same observable behavior, fewer operations).

### 1. Remove the superfluous comment

Delete the comment `/* VS16 does not change emoji state */` in `_PyUnicode_ScanIdentifier`. It restates what the code already shows. Pure deletion.

**Files:** `Objects/unicodeobject.c`

### 2. Fix the misleading ZWJ comment

Reword `/* Constrained ZWJ: only allow ZWJ between emoji */` — ZWJ is also allowed after non-emoji for Indic scripts (and the code already handles this). The comment should reflect the actual logic: ZWJ is intercepted early to enforce emoji-only context, but falls through to XID_Continue when not preceded by emoji.

**Files:** `Objects/unicodeobject.c`

### 3. Add named constants for ZWJ and VS16

Replace the magic numbers `0x200D` (ZWJ) and `0xFE0F` (VS16) with `#define` constants in the header. Currently they appear with inline comments in `_PyUnicode_ScanIdentifier`; the named constants make the code self-documenting.

**Files:** `Include/internal/pycore_unicodeobject.h`, `Objects/unicodeobject.c`

### 4. Rename `EMOJI_MISC_TECH_FF` and `EMOJI_MISC_TECH_REW`

These abbreviations are unclear. Rename to self-documenting names (e.g., `EMOJI_MISC_TECH_FAST_FORWARD`, `EMOJI_MISC_TECH_REWIND` or similar).

**Files:** `Include/internal/pycore_unicodeobject.h`

### 5. Rename the sub-range constants

Replace abbreviated names like `EMOJI_MSA_SUB1_START`, `EMOJI_GEO_EXT_SUB*`, `EMOJI_EXT_A_SUB*` with fewer abbreviations and more self-documenting names, following Approach B's naming conventions. For example, `EMOJI_MISC_SYMB_ARROWS_SUB1_START` instead of `EMOJI_MSA_SUB1_START`.

**Files:** `Include/internal/pycore_unicodeobject.h`

### 6. Fix `prev_was_emoji` naming

At initialization (line 12418 of `unicodeobject.c`), `prev_was_emoji` captures the *current* character's emoji status, not the previous one. Rename or restructure to eliminate the misleading semantics. One option: rename to `last_emoji_status` or restructure so the variable is only set inside the loop where "previous" is accurate.

**Files:** `Objects/unicodeobject.c`

### 7. Update `extern` declarations for `IsXidStart`/`IsXidContinue`

The `extern` declarations of `_PyUnicode_IsXidStart` and `_PyUnicode_IsXidContinue` in `pycore_unicodeobject.h` don't mention that they now include emoji extension behavior. Add a brief comment documenting that these functions return 1 for emoji characters in addition to standard XID characters.

**Files:** `Include/internal/pycore_unicodeobject.h`

### 8. Add an outer range guard to `_PyUnicode_IsEmoji`

Add `if (ch < 0x231A) return 0;` (using the named constant `EMOJI_MISC_TECH_WATCH`) at the top of `_PyUnicode_IsEmoji`. This rejects all characters below the lowest emoji codepoint in a single comparison, avoiding the full cascade of range checks for ASCII and common non-ASCII characters.

**Files:** `Include/internal/pycore_unicodeobject.h`

**Expected benchmark impact:** "Non-ASCII below emoji range" category should show a measurable drop (characters like `é`, `α`, `б` currently fall through ~22 comparisons before returning 0; the guard makes it one comparison).

### 9. Add an ASCII fast-path before `_PyUnicode_IsEmoji`

Currently `_PyUnicode_IsEmoji` is called for every character including ASCII, which is wasted work for the overwhelmingly common case. Add an `if (ch < 0x80)` guard before calling `_PyUnicode_IsEmoji` in `_PyUnicode_IsXidStart`, `_PyUnicode_IsXidContinue` (both already have ASCII fast-paths that return early — but the emoji check on line 88/99 of `unicodectype.c` is evaluated after the `gettyperecord` lookup, not guarded by the ASCII early return). Verify that the existing ASCII early-return in each function already prevents the `_PyUnicode_IsEmoji` call from being reached for ASCII characters; if not, restructure so it does.

**Files:** `Objects/unicodectype.c`

**Expected benchmark impact:** "Pure ASCII" category should show a measurable drop if ASCII characters are currently reaching the `_PyUnicode_IsEmoji` call.

### 10. Back-port the double-eval fix from commit `4200a3b9611`

`_PyUnicode_ScanIdentifier` calls `_PyUnicode_IsEmoji(ch)` on line 12446, then `_PyUnicode_IsXidContinue(ch)` on line 12447, which internally calls `_PyUnicode_IsEmoji(ch)` again. The fix from commit `4200a3b9611` on the main branch eliminates this redundant evaluation. Apply the same fix to the Approach A worktree.

**Files:** `Objects/unicodeobject.c`, potentially `Objects/unicodectype.c`

**Expected benchmark impact:** "SMP emoji" and "Mixed ASCII + emoji" categories should show a measurable drop (SMP emoji require many comparisons per `_PyUnicode_IsEmoji` call, so eliminating the duplicate call saves the most for these characters).

---

## Refactoring Results

All 10 refactors were applied to the Approach A worktree (`emoji-v02-approach-a`). All 103 tests passed (6 skipped) after every change.

### Cosmetic Refactors (1–7)

| # | Refactor | Commit | Files |
|---|----------|--------|-------|
| 1 | Removed superfluous "VS16 does not change emoji state" comment | `bc900375d6d` | `unicodeobject.c` |
| 2 | Fixed misleading ZWJ comment to reflect actual behavior | `185857756c4` | `unicodeobject.c` |
| 3 | Added named constants `EMOJI_ZERO_WIDTH_JOINER` and `EMOJI_VARIATION_SELECTOR_16` | `111568f8f9a` | `pycore_unicodeobject.h`, `unicodeobject.c` |
| 4 | Renamed `EMOJI_MISC_TECH_FF`/`REW` → `FAST_FORWARD`/`REWIND` | `15d66d89508` | `pycore_unicodeobject.h` |
| 5 | Renamed `MSA`→`MISC_SYMB_ARROWS`, `GEO_EXT`→`GEOMETRIC_EXT`, `EXT_A`→`EXTENDED_A` | `eaa59d70d36` | `pycore_unicodeobject.h` |
| 6 | Renamed `prev_was_emoji` → `last_was_emoji` | `43fd3def848` | `unicodeobject.c` |
| 7 | Documented emoji extension on `IsXidStart`/`IsXidContinue` declarations | `b253c11f2cc` | `pycore_unicodeobject.h` |

### Performance Refactors (8–10)

Each change was benchmarked with `bench_emoji_identifiers.py` at 1,000,000 iterations per test string before and after the change. Only changes that produced a measurable speedup were committed.

#### Change 8: Range guard at top of `_PyUnicode_IsEmoji`

Added `if (ch < EMOJI_MISC_TECH_WATCH) return 0;` to reject all characters below the lowest emoji codepoint in a single comparison.

| Commit | `08b61e19506` |
|--------|---------------|

| Test | Before | After | Change |
|------|--------|-------|--------|
| latin_accent (`café`) | 47.4 ns | 45.7 ns | -3.6% |
| greek_word (`αβγ`) | 45.8 ns | 41.5 ns | -9.4% |
| cyrillic_word (`буква`) | 53.5 ns | 47.8 ns | -10.7% |
| mixed_latin (`naïve_résumé`) | 78.3 ns | 75.3 ns | -3.8% |
| ascii_underscore | 82.8 ns | 76.7 ns | -7.4% |
| ascii_long | 159.4 ns | 149.5 ns | -6.2% |
| emoji_then_ascii | 74.4 ns | 54.0 ns | -27.4% |

#### Change 9: ASCII fast-path in `ScanIdentifier`

Added `(ch >= 0x80) ? _PyUnicode_IsEmoji(ch) : 0` guards to skip calling `_PyUnicode_IsEmoji` entirely for ASCII characters.

| Commit | `230441b2baa` |
|--------|---------------|

| Test | Before (post-8) | After | Change |
|------|-----------------|-------|--------|
| ascii_underscore | 76.7 ns | 69.4 ns | -9.5% |
| ascii_long | 149.5 ns | 137.5 ns | -8.0% |
| emoji_then_ascii | 54.0 ns | 47.8 ns | -11.5% |
| long_ascii_one_emoji | 106.1 ns | 85.6 ns | -19.3% |
| emoji_ascii_emoji | 61.1 ns | 55.4 ns | -9.3% |

#### Change 10: Eliminate double `_PyUnicode_IsEmoji` eval

Added `_PyUnicode_IsXidContinueNoEmoji` — a variant of `_PyUnicode_IsXidContinue` that checks only standard XID properties without calling `_PyUnicode_IsEmoji`. Used in `ScanIdentifier` where the emoji status is already computed separately.

| Commit | `805c6f3d95b` |
|--------|---------------|

| Test | Before (post-9) | After | Change |
|------|-----------------|-------|--------|
| ascii_word | 57.5 ns | 51.1 ns | -11.1% |
| ascii_underscore | 69.4 ns | 62.8 ns | -9.5% |
| ascii_long | 137.5 ns | 111.4 ns | -19.0% |
| latin_accent | 47.1 ns | 44.8 ns | -4.9% |
| mixed_latin | 73.8 ns | 70.2 ns | -4.9% |
| smp_sequence | 48.3 ns | 45.7 ns | -5.4% |

### Cumulative Performance Improvement (Original → Final)

| Test | Original | Final | Total speedup |
|------|----------|-------|--------------|
| ascii_long | 159.4 ns | 111.4 ns | **-30.1%** |
| ascii_underscore | 82.8 ns | 62.8 ns | **-24.2%** |
| long_ascii_one_emoji | 113.0 ns | 82.5 ns | **-27.0%** |
| cyrillic_word | 53.5 ns | 51.0 ns | **-4.7%** |
| smp_sequence | 54.2 ns | 45.7 ns | **-15.7%** |
| emoji_then_ascii | 74.4 ns | 47.2 ns | **-36.6%** |
