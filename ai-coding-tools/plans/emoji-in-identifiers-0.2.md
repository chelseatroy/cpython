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
