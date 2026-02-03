/*
   Unicode character type helpers.

   Written by Marc-Andre Lemburg (mal@lemburg.com).
   Modified for Python 2.0 by Fredrik Lundh (fredrik@pythonware.com)

   Copyright (c) Corporation for National Research Initiatives.

*/

#include "Python.h"

#define ALPHA_MASK 0x01
#define DECIMAL_MASK 0x02
#define DIGIT_MASK 0x04
#define LOWER_MASK 0x08
#define TITLE_MASK 0x40
#define UPPER_MASK 0x80
#define XID_START_MASK 0x100
#define XID_CONTINUE_MASK 0x200
#define PRINTABLE_MASK 0x400
#define NUMERIC_MASK 0x800
#define CASE_IGNORABLE_MASK 0x1000
#define CASED_MASK 0x2000
#define EXTENDED_CASE_MASK 0x4000

typedef struct {
    /*
       These are either deltas to the character or offsets in
       _PyUnicode_ExtendedCase.
    */
    const int upper;
    const int lower;
    const int title;
    /* Note if more flag space is needed, decimal and digit could be unified. */
    const unsigned char decimal;
    const unsigned char digit;
    const unsigned short flags;
} _PyUnicode_TypeRecord;

#include "unicodetype_db.h"

static const _PyUnicode_TypeRecord *
gettyperecord(Py_UCS4 code)
{
    int index;

    if (code >= 0x110000)
        index = 0;
    else
    {
        index = index1[(code>>SHIFT)];
        index = index2[(index<<SHIFT)+(code&((1<<SHIFT)-1))];
    }

    return &_PyUnicode_TypeRecords[index];
}

/* Returns the titlecase Unicode characters corresponding to ch or just
   ch if no titlecase mapping is known. */

Py_UCS4 _PyUnicode_ToTitlecase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK)
        return _PyUnicode_ExtendedCase[ctype->title & 0xFFFF];
    return ch + ctype->title;
}

/* Returns 1 for Unicode characters having the category 'Lt', 0
   otherwise. */

int _PyUnicode_IsTitlecase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & TITLE_MASK) != 0;
}

/* Returns 1 if ch is an emoji codepoint that should be allowed in identifiers.

   This function checks various Unicode ranges that contain emoji characters.
   The ranges are based on Unicode emoji data and include:
   - Miscellaneous Symbols (U+2600-U+26FF)
   - Dingbats (U+2700-U+27BF)
   - Miscellaneous Symbols and Pictographs (U+1F300-U+1F5FF)
   - Emoticons (U+1F600-U+1F64F)
   - Transport and Map Symbols (U+1F680-U+1F6FF)
   - Supplemental Symbols and Pictographs (U+1F900-U+1F9FF)
   - Symbols and Pictographs Extended-A (U+1FA00-U+1FAFF)
   - Skin tone modifiers (U+1F3FB-U+1F3FF)
*/
static int
_PyUnicode_IsEmoji(Py_UCS4 ch)
{
    /* Miscellaneous Symbols (U+2600-U+26FF) */
    if (ch >= 0x2600 && ch <= 0x26FF)
        return 1;

    /* Dingbats (U+2700-U+27BF) */
    if (ch >= 0x2700 && ch <= 0x27BF)
        return 1;

    /* Miscellaneous Symbols and Pictographs (U+1F300-U+1F5FF) */
    if (ch >= 0x1F300 && ch <= 0x1F5FF)
        return 1;

    /* Emoticons (U+1F600-U+1F64F) */
    if (ch >= 0x1F600 && ch <= 0x1F64F)
        return 1;

    /* Transport and Map Symbols (U+1F680-U+1F6FF) */
    if (ch >= 0x1F680 && ch <= 0x1F6FF)
        return 1;

    /* Supplemental Symbols and Pictographs (U+1F900-U+1F9FF) */
    if (ch >= 0x1F900 && ch <= 0x1F9FF)
        return 1;

    /* Symbols and Pictographs Extended-A (U+1FA00-U+1FAFF) */
    if (ch >= 0x1FA00 && ch <= 0x1FAFF)
        return 1;

    /* Skin tone modifiers (U+1F3FB-U+1F3FF) */
    if (ch >= 0x1F3FB && ch <= 0x1F3FF)
        return 1;

    return 0;
}

/* Returns 1 for Unicode characters having the XID_Start property, 0
   otherwise. Also returns 1 for emoji characters that can start identifiers. */

int _PyUnicode_IsXidStart(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & XID_START_MASK) != 0 || _PyUnicode_IsEmoji(ch);
}

/* Returns 1 for Unicode characters having the XID_Continue property,
   0 otherwise. Also returns 1 for emoji characters and emoji-related
   modifier characters that can continue identifiers.

   This includes:
   - All emoji characters (via _PyUnicode_IsEmoji)
   - Zero Width Joiner (U+200D) for ZWJ emoji sequences
   - Variation Selector 16 (U+FE0F) for emoji presentation
*/

int _PyUnicode_IsXidContinue(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if ((ctype->flags & XID_CONTINUE_MASK) != 0)
        return 1;

    /* Allow emoji characters */
    if (_PyUnicode_IsEmoji(ch))
        return 1;

    /* Allow Zero Width Joiner (U+200D) for ZWJ emoji sequences */
    if (ch == 0x200D)
        return 1;

    /* Allow Variation Selector 16 (U+FE0F) for emoji presentation */
    if (ch == 0xFE0F)
        return 1;

    return 0;
}

/* Returns the integer decimal (0-9) for Unicode characters having
   this property, -1 otherwise. */

int _PyUnicode_ToDecimalDigit(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & DECIMAL_MASK) ? ctype->decimal : -1;
}

int _PyUnicode_IsDecimalDigit(Py_UCS4 ch)
{
    if (_PyUnicode_ToDecimalDigit(ch) < 0)
        return 0;
    return 1;
}

/* Returns the integer digit (0-9) for Unicode characters having
   this property, -1 otherwise. */

int _PyUnicode_ToDigit(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & DIGIT_MASK) ? ctype->digit : -1;
}

int _PyUnicode_IsDigit(Py_UCS4 ch)
{
    if (_PyUnicode_ToDigit(ch) < 0)
        return 0;
    return 1;
}

/* Returns the numeric value as double for Unicode characters having
   this property, -1.0 otherwise. */

int _PyUnicode_IsNumeric(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & NUMERIC_MASK) != 0;
}

/* Returns 1 for Unicode characters that repr() may use in its output,
   and 0 for characters to be hex-escaped.

   See documentation of `str.isprintable` for details.
*/
int _PyUnicode_IsPrintable(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & PRINTABLE_MASK) != 0;
}

/* Returns 1 for Unicode characters having the category 'Ll', 0
   otherwise. */

int _PyUnicode_IsLowercase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & LOWER_MASK) != 0;
}

/* Returns 1 for Unicode characters having the category 'Lu', 0
   otherwise. */

int _PyUnicode_IsUppercase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & UPPER_MASK) != 0;
}

/* Returns the uppercase Unicode characters corresponding to ch or just
   ch if no uppercase mapping is known. */

Py_UCS4 _PyUnicode_ToUppercase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK)
        return _PyUnicode_ExtendedCase[ctype->upper & 0xFFFF];
    return ch + ctype->upper;
}

/* Returns the lowercase Unicode characters corresponding to ch or just
   ch if no lowercase mapping is known. */

Py_UCS4 _PyUnicode_ToLowercase(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK)
        return _PyUnicode_ExtendedCase[ctype->lower & 0xFFFF];
    return ch + ctype->lower;
}

int _PyUnicode_ToLowerFull(Py_UCS4 ch, Py_UCS4 *res)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK) {
        int index = ctype->lower & 0xFFFF;
        int n = ctype->lower >> 24;
        int i;
        for (i = 0; i < n; i++)
            res[i] = _PyUnicode_ExtendedCase[index + i];
        return n;
    }
    res[0] = ch + ctype->lower;
    return 1;
}

int _PyUnicode_ToTitleFull(Py_UCS4 ch, Py_UCS4 *res)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK) {
        int index = ctype->title & 0xFFFF;
        int n = ctype->title >> 24;
        int i;
        for (i = 0; i < n; i++)
            res[i] = _PyUnicode_ExtendedCase[index + i];
        return n;
    }
    res[0] = ch + ctype->title;
    return 1;
}

int _PyUnicode_ToUpperFull(Py_UCS4 ch, Py_UCS4 *res)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK) {
        int index = ctype->upper & 0xFFFF;
        int n = ctype->upper >> 24;
        int i;
        for (i = 0; i < n; i++)
            res[i] = _PyUnicode_ExtendedCase[index + i];
        return n;
    }
    res[0] = ch + ctype->upper;
    return 1;
}

int _PyUnicode_ToFoldedFull(Py_UCS4 ch, Py_UCS4 *res)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    if (ctype->flags & EXTENDED_CASE_MASK && (ctype->lower >> 20) & 7) {
        int index = (ctype->lower & 0xFFFF) + (ctype->lower >> 24);
        int n = (ctype->lower >> 20) & 7;
        int i;
        for (i = 0; i < n; i++)
            res[i] = _PyUnicode_ExtendedCase[index + i];
        return n;
    }
    return _PyUnicode_ToLowerFull(ch, res);
}

int _PyUnicode_IsCased(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & CASED_MASK) != 0;
}

int _PyUnicode_IsCaseIgnorable(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & CASE_IGNORABLE_MASK) != 0;
}

/* Returns 1 for Unicode characters having the category 'Ll', 'Lu', 'Lt',
   'Lo' or 'Lm',  0 otherwise. */

int _PyUnicode_IsAlpha(Py_UCS4 ch)
{
    const _PyUnicode_TypeRecord *ctype = gettyperecord(ch);

    return (ctype->flags & ALPHA_MASK) != 0;
}

