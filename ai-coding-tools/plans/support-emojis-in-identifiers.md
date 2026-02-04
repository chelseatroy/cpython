# Plan: Support Emojis in Python Identifiers

## Goal
Allow emoji characters in variable, function, and class names. Emojis can start or continue identifiers, like letters.

## Architecture: Current Flow
```
Source Code --> Lexer (Parser/lexer/lexer.c)
                 |
                 | byte >= 128? pass as potential identifier
                 v
               verify_identifier()
                 |
                 v
               _PyUnicode_ScanIdentifier() (Objects/unicodeobject.c)
                 |
                 | char 0: _PyUnicode_IsXidStart(ch) || ch == '_'
                 | char 1+: _PyUnicode_IsXidContinue(ch)
                 v
               unicodectype.c: checks XID_START_MASK / XID_CONTINUE_MASK
                 |
                 v
               Emoji codepoints have NEITHER flag set --> REJECTED
```

---

## Multi-Agent Execution Strategy

We will use git worktrees to run multiple implementation approaches in parallel. Each agent works on a separate branch, all starting from a shared test suite.

### Git Worktree Setup

```bash
# From the main cpython repo, create worktrees for each approach:
git worktree add ../cpython-approach-a -b emoji-approach-a
git worktree add ../cpython-approach-b -b emoji-approach-b
git worktree add ../cpython-approach-c -b emoji-approach-c
```

---

## Phase 1: Shared Test Suite (Execute First, Before Branching)

Create `Lib/test/test_emoji_identifiers.py` with comprehensive tests that all approaches must pass.

### 1.1 New Feature Tests (should PASS after implementation)

| Test Name | Description |
|-----------|-------------|
| `test_emoji_identifier__single_emoji_as_variable__assigns_successfully` | `🎉 = 1; assert 🎉 == 1` |
| `test_emoji_identifier__emoji_starting_name_with_ascii__assigns_successfully` | `🎉party = 1` |
| `test_emoji_identifier__emoji_in_continuation__assigns_successfully` | `my🎉var = 1` |
| `test_emoji_identifier__emoji_as_function_name__defines_successfully` | `def 🎉(): return 1` |
| `test_emoji_identifier__emoji_as_class_name__defines_successfully` | `class 🎉: pass` |
| `test_emoji_identifier__str_isidentifier__returns_true` | `assert "🎉".isidentifier()` |
| `test_emoji_identifier__misc_symbols_range__valid` | Test U+2600-U+26FF (☀, ⚡, etc.) |
| `test_emoji_identifier__dingbats_range__valid` | Test U+2700-U+27BF (✂, ✈, etc.) |
| `test_emoji_identifier__emoticons_range__valid` | Test U+1F600-U+1F64F (😀, 😎, etc.) |
| `test_emoji_identifier__transport_range__valid` | Test U+1F680-U+1F6FF (🚀, 🛸, etc.) |
| `test_emoji_identifier__supplemental_range__valid` | Test U+1F900-U+1F9FF (🤖, 🧠, etc.) |
| `test_emoji_identifier__extended_a_range__valid` | Test U+1FA00-U+1FAFF (🪐, 🫠, etc.) |

### 1.2 ZWJ Sequence Tests (behavior varies by approach)

| Test Name | Description |
|-----------|-------------|
| `test_emoji_identifier__zwj_family_sequence__forms_single_identifier` | 👨‍👩‍👧 (family emoji) |
| `test_emoji_identifier__zwj_profession_sequence__forms_single_identifier` | 👨‍💻 (man technologist) |
| `test_emoji_identifier__zwj_flag_sequence__forms_single_identifier` | 🏳️‍🌈 |

### 1.3 Edge Cases

| Test Name | Description |
|-----------|-------------|
| `test_emoji_identifier__skin_tone_modifier__valid_continuation` | 👋🏽 (wave + skin tone) |
| `test_emoji_identifier__variation_selector_16__valid_continuation` | Emoji with VS16 |
| `test_emoji_identifier__multiple_emoji_in_name__valid` | `🎉🚀🔥 = 1` |
| `test_emoji_identifier__emoji_with_underscore__valid` | `_🎉` and `🎉_` |
| `test_emoji_identifier__emoji_with_numbers__valid` | `🎉123` (emoji start, number continue) |

### 1.4 Backward Compatibility Tests (must PASS - existing valid Python must still work)

| Test Name | Description |
|-----------|-------------|
| `test_backward_compat__ascii_identifiers__still_valid` | `foo`, `_bar`, `baz123` |
| `test_backward_compat__unicode_letters__still_valid` | `café`, `日本語`, `Ω` |
| `test_backward_compat__underscore_start__still_valid` | `_private`, `__dunder__` |
| `test_backward_compat__digit_cannot_start__still_raises` | `1foo` raises SyntaxError |
| `test_backward_compat__operators_rejected__still_raises` | `+`, `-`, `@` raise SyntaxError |
| `test_backward_compat__existing_isidentifier_true__unchanged` | `"foo".isidentifier()` still True |
| `test_backward_compat__existing_isidentifier_false__unchanged` | `"123".isidentifier()` still False |

### 1.5 Negative Tests (should still FAIL/raise errors)

| Test Name | Description |
|-----------|-------------|
| `test_negative__digit_start_with_emoji__raises` | `1🎉` should raise SyntaxError |
| `test_negative__operator_chars__raises` | `+`, `=`, `@` not valid |
| `test_negative__whitespace__raises` | Space in identifier not valid |

---

## Phase 2: Parallel Implementation Approaches (in separate worktrees)

### Approach A: Modify unicodectype.c (simplest)
**Branch:** `emoji-approach-a`
**Worktree:** `../cpython-approach-a`

Modify `_PyUnicode_IsXidStart` and `_PyUnicode_IsXidContinue` to also check emoji ranges.
- ZWJ handling: Allow globally as continuation character
- Emoji ranges: Broad block-based ranges

```c
// In Objects/unicodectype.c
static int _PyUnicode_IsEmoji(Py_UCS4 ch) { /* range checks */ }

int _PyUnicode_IsXidStart(Py_UCS4 ch) {
    return (ctype->flags & XID_START_MASK) != 0 || _PyUnicode_IsEmoji(ch);
}

int _PyUnicode_IsXidContinue(Py_UCS4 ch) {
    return (ctype->flags & XID_CONTINUE_MASK) != 0
        || _PyUnicode_IsEmoji(ch) || ch == 0x200D || ch == 0xFE0F;
}
```

### Approach B: Modify makeunicodedata.py (cleanest integration)
**Branch:** `emoji-approach-b`
**Worktree:** `../cpython-approach-b`

Modify `Tools/unicode/makeunicodedata.py` to add emoji codepoints to XID_Start/XID_Continue flags in the generated tables.
- ZWJ handling: Do not add ZWJ to tables (ZWJ sequences won't work as single identifiers)
- Emoji ranges: Read from Unicode emoji-data.txt for precision

### Approach C: Modify _PyUnicode_ScanIdentifier (most control)
**Branch:** `emoji-approach-c`
**Worktree:** `../cpython-approach-c`

Modify `Objects/unicodeobject.c:_PyUnicode_ScanIdentifier()` to have emoji-aware scanning logic.
- ZWJ handling: Only allow ZWJ when preceded by emoji codepoint (constrained)
- Emoji ranges: Precise checking with context awareness

---

## Phase 3: Build and Test Each Approach

In each worktree:
```bash
./configure --with-pydebug
make -j4
./python -m test test_emoji_identifiers -v
make test  # Full test suite for regression check
```

---

## Phase 4: Compare Results

Each approach reports:
1. Which tests pass/fail
2. Build complexity
3. Lines of code changed
4. Any unexpected side effects discovered

## Risks and Considerations

### Why CPython doesn't allow emojis currently

1. **Unicode Standard compliance.** Python follows UAX #31 (Unicode Identifier and Pattern Syntax), which uses XID_Start/XID_Continue properties. Emojis are category "So" (Symbol, Other), deliberately excluded from these properties by the Unicode Consortium.

2. **Visual ambiguity.** Emojis render differently across platforms, fonts, and OS versions. The same codepoint can look quite different on macOS vs Windows vs a terminal, making code harder to read and review reliably.

3. **Multi-codepoint complexity.** Many "single emojis" are actually sequences of 2-7 codepoints (ZWJ sequences, flag sequences, skin tone variants).

4. **Homoglyph/confusion attacks.** Some emojis look similar to each other (e.g., different heart colors), creating opportunities for confusing or malicious code.

5. **Tooling ecosystem.** Linters, formatters, IDEs, syntax highlighters, debuggers, and documentation tools assume identifiers follow XID rules. Emoji identifiers may break or confuse these tools.

### Risks specific to this plan

| Risk | Severity | Description |
|------|----------|-------------|
| **ZWJ as continuation character** | HIGH | Allowing ZWJ (U+200D) globally means `a‍b` (a + ZWJ + b) becomes a valid identifier distinct from `ab`. ZWJ is used in Indic scripts, Arabic, and other writing systems — not just emoji. This could enable confusing identifiers. |
| **Overly broad emoji ranges** | MEDIUM | The U+2600-U+26FF and U+2700-U+27BF blocks include non-emoji symbols (e.g., ⚊ hexagram, ✁ scissors) that might be surprising as identifier characters. |
| **`str.isidentifier()` behavior change** | MEDIUM | Code relying on `str.isidentifier()` for validation or security checks will now accept emoji strings, with potential downstream effects in frameworks or libraries. |
| **Existing test failures** | LOW | Some tests may explicitly assert that emoji are *not* valid identifiers and would need updating. |
| **VS16 (U+FE0F) ambiguity** | LOW | Variation Selector 16 changes text rendering to emoji rendering. Allowing it means `x` and `x️` (with VS16) could be different identifiers. |

### Possible mitigations

- **Constrained ZWJ:** Only allow ZWJ when preceded by an emoji codepoint. This requires modifying `_PyUnicode_ScanIdentifier()` instead of just the character-check functions.
- **Narrower emoji ranges:** Use Unicode's official emoji-data.txt to define exactly which codepoints are emoji, rather than broad block ranges.
- **Documentation:** Clearly document this as a CPython extension beyond standard Python/Unicode behavior.

---

## Phase 5: Approach Selection

### Decision: Approach C Selected

We evaluated four implementation approaches across worktrees:

| Worktree | Approach | Description |
|----------|----------|-------------|
| `../cpython-approach-a` | A | Broad ranges + explicit ZWJ/VS16 in `unicodectype.c` |
| `../cpython-approach-b` | B | Broad ranges, emoji-only in `unicodectype.c` (no explicit ZWJ/VS16) |
| `../cpython-approach-c` | **C (selected)** | Broad ranges + context-aware VS16 in `_PyUnicode_ScanIdentifier` |
| `../cpython-approach-d` | D | Narrow ranges + explicit ZWJ/VS16 in `unicodectype.c` |

### Key finding during implementation

ZWJ (U+200D) is natively in `XID_Continue` per the Unicode standard because it is used for Indic script conjunct consonants. VS16 (U+FE0F) is also natively in `XID_Continue` as a Variation Selector (category Mn). This means all approaches that add emoji to `XID_Start` automatically get ZWJ sequence support — it cannot be disabled without breaking Indic scripts.

### Reasons for selecting Approach C

1. **Covers all emoji.** Uses broad block-based ranges (1,936 codepoints), covering 100% of commonly used emoji including newer Extended-A additions like 🪐 and 🫠. Approach D's narrow ranges missed ~10% of popular emoji and would fall further behind as Unicode adds new emoji.

2. **Prevents confusing VS16 variants of text characters.** Approach C is the only approach that rejects VS16 (U+FE0F) after non-emoji characters. In approaches A, B, and D, `a` and `a️` (a + VS16) would be two distinct valid identifiers that look identical in most rendering contexts. Approach C's context-aware scanning in `_PyUnicode_ScanIdentifier()` only allows VS16 when the preceding character is an emoji, preventing this class of confusing homoglyph.

### Approaches not selected

- **Approach A:** Simplest (22 insertions, 1 file), but allows VS16 after any character, creating confusing identifier variants.
- **Approach B:** Originally intended to modify `makeunicodedata.py` for table-level integration, but regenerating Unicode tables requires downloading data files from unicode.org (HTTP 403). Fell back to a unicodectype.c-only variant. Same VS16 problem as A.
- **Approach D:** Narrower ranges reduce the "surface area" of non-emoji symbols accepted, but miss commonly used emoji (🪐, 🫠, 🛸) and would require ongoing maintenance as Unicode adds new emoji blocks.
