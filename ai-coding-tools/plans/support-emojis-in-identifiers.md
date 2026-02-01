# Plan: Support Emojis in Python Identifiers

## Goal
Allow emoji characters in variable, function, and class names. Emojis can start or continue identifiers, like letters.

## Architecture: Current vs. Proposed

### Current Flow
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

### Proposed Flow
```
Same pipeline, but in unicodectype.c:

  _PyUnicode_IsXidStart(ch)    --> also returns 1 if _PyUnicode_IsEmoji(ch)
  _PyUnicode_IsXidContinue(ch) --> also returns 1 if _PyUnicode_IsEmoji(ch)
                                   OR ch == 0x200D (ZWJ)
                                   OR ch == 0xFE0F (VS16)

No lexer changes needed (bytes >= 128 already accepted).
```

## Files to Modify

| File | Change |
|------|--------|
| `Objects/unicodectype.c` | Add `_PyUnicode_IsEmoji()` helper; modify `IsXidStart` and `IsXidContinue` |
| `Lib/test/test_emoji_identifiers.py` | New test file |

## Implementation Steps

### Step 1: Write tests (`Lib/test/test_emoji_identifiers.py`)

Tests following `subject__situation__result` naming:

- `test_emoji_identifier__single_emoji_as_variable__assigns_successfully`
- `test_emoji_identifier__emoji_starting_name_with_ascii__assigns_successfully`
- `test_emoji_identifier__emoji_in_continuation__assigns_successfully`
- `test_emoji_identifier__emoji_as_function_name__defines_successfully`
- `test_emoji_identifier__emoji_as_class_name__defines_successfully`
- `test_emoji_identifier__str_isidentifier__returns_true`
- `test_emoji_identifier__various_emoji_ranges__all_valid` (U+2600s, U+1F300s, U+1F600s, U+1FA00s)
- `test_emoji_identifier__zwj_sequence__forms_single_identifier`
- `test_emoji_identifier__digit_still_cannot_start__raises_syntax_error`

### Step 2: Add `_PyUnicode_IsEmoji()` in `Objects/unicodectype.c`

```c
static int
_PyUnicode_IsEmoji(Py_UCS4 ch)
{
    if (ch >= 0x2600 && ch <= 0x26FF) return 1;  /* Misc Symbols */
    if (ch >= 0x2700 && ch <= 0x27BF) return 1;  /* Dingbats */
    if (ch >= 0x1F000 && ch <= 0x1F02F) return 1; /* Mahjong/Dominos */
    if (ch >= 0x1F300 && ch <= 0x1F9FF) return 1; /* Main emoji blocks */
    if (ch >= 0x1FA00 && ch <= 0x1FAFF) return 1; /* Extended-A */
    return 0;
}
```

### Step 3: Modify `_PyUnicode_IsXidStart` and `_PyUnicode_IsXidContinue`

```c
int _PyUnicode_IsXidStart(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);
    return (ctype->flags & XID_START_MASK) != 0 || _PyUnicode_IsEmoji(ch);
}

int _PyUnicode_IsXidContinue(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);
    return (ctype->flags & XID_CONTINUE_MASK) != 0
        || _PyUnicode_IsEmoji(ch)
        || ch == 0x200D   /* ZWJ for multi-codepoint emoji */
        || ch == 0xFE0F;  /* Variation Selector 16 */
}
```

### Step 4: Build and verify

```bash
./configure --with-pydebug
make
./python -m test test_emoji_identifiers
```

## Verification

1. Build CPython with the changes
2. Run the new test suite: `./python -m test test_emoji_identifiers`
3. Run existing tests to confirm nothing breaks: `make test`
4. Manual smoke test in REPL: `🎉 = "party"` and `print(🎉)`
