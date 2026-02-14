#ifndef Py_INTERNAL_UNICODEOBJECT_H
#define Py_INTERNAL_UNICODEOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif

#ifndef Py_BUILD_CORE
#  error "this header requires Py_BUILD_CORE define"
#endif

#include "pycore_fileutils.h"     // _Py_error_handler
#include "pycore_ucnhash.h"       // _PyUnicode_Name_CAPI

/* --- Characters Type APIs ----------------------------------------------- */

/* Sequence-joining and variation characters used in emoji identifiers. */
#define EMOJI_ZERO_WIDTH_JOINER        0x200D
#define EMOJI_VARIATION_SELECTOR_16    0xFE0F

/* Cherry-picked Miscellaneous Technical characters (U+2300..U+23FF). */
#define EMOJI_MISC_TECH_WATCH          0x231A
#define EMOJI_MISC_TECH_HOURGLASS      0x231B
#define EMOJI_MISC_TECH_FF             0x23E9
#define EMOJI_MISC_TECH_REW            0x23EA
#define EMOJI_MISC_TECH_UP             0x23EB
#define EMOJI_MISC_TECH_DOWN           0x23EC
#define EMOJI_MISC_TECH_ALARM          0x23F0
#define EMOJI_MISC_TECH_HOURGLASS2     0x23F3

/* Fully assigned BMP blocks. */
#define EMOJI_GEOMETRIC_SHAPES_START   0x25A0
#define EMOJI_GEOMETRIC_SHAPES_END     0x25FF
#define EMOJI_MISC_SYMBOLS_START       0x2600
#define EMOJI_DINGBATS_END             0x27BF

/* Misc Symbols and Arrows (U+2B00..U+2BFF): 3 assigned sub-ranges.
   Gaps: U+2B74..U+2B75, U+2B96. */
#define EMOJI_MSA_SUB1_START           0x2B00
#define EMOJI_MSA_SUB1_END             0x2B73
#define EMOJI_MSA_SUB2_START           0x2B76
#define EMOJI_MSA_SUB2_END             0x2B95
#define EMOJI_MSA_SUB3_START           0x2B97
#define EMOJI_MSA_SUB3_END             0x2BFF

/* Fully assigned SMP blocks. */
#define EMOJI_REGIONAL_IND_START       0x1F1E6
#define EMOJI_REGIONAL_IND_END         0x1F1FF
#define EMOJI_MISC_PICTOGRAPHS_START   0x1F300
#define EMOJI_MISC_PICTOGRAPHS_END     0x1F5FF
#define EMOJI_EMOTICONS_START          0x1F600
#define EMOJI_EMOTICONS_END            0x1F64F
#define EMOJI_SUPPLEMENTAL_START       0x1F900
#define EMOJI_SUPPLEMENTAL_END         0x1F9FF

/* Transport and Map Symbols (U+1F680..U+1F6FF): 3 assigned sub-ranges.
   Gaps: U+1F6D8..U+1F6DB, U+1F6ED..U+1F6EF. */
#define EMOJI_TRANSPORT_SUB1_START     0x1F680
#define EMOJI_TRANSPORT_SUB1_END       0x1F6D7
#define EMOJI_TRANSPORT_SUB2_START     0x1F6DC
#define EMOJI_TRANSPORT_SUB2_END       0x1F6EC
#define EMOJI_TRANSPORT_SUB3_START     0x1F6F0
#define EMOJI_TRANSPORT_SUB3_END       0x1F6FC

/* Geometric Shapes Extended (U+1F780..U+1F7FF): 3 assigned sub-ranges.
   Gaps: U+1F7DA..U+1F7DF, U+1F7EC..U+1F7EF. */
#define EMOJI_GEO_EXT_SUB1_START      0x1F780
#define EMOJI_GEO_EXT_SUB1_END        0x1F7D9
#define EMOJI_GEO_EXT_SUB2_START      0x1F7E0
#define EMOJI_GEO_EXT_SUB2_END        0x1F7EB
#define EMOJI_GEO_EXT_SUB3_START      0x1F7F0
#define EMOJI_GEO_EXT_SUB3_END        0x1F7F0

/* Symbols and Pictographs Extended-A (U+1FA00..U+1FAFF): 8 assigned sub-ranges.
   Gaps: U+1FA54..U+1FA5F, U+1FA6E..U+1FA6F, U+1FA7D..U+1FA7F,
         U+1FA8A..U+1FA8E, U+1FAC7..U+1FACD, U+1FADD..U+1FADE,
         U+1FAEA..U+1FAEF. */
#define EMOJI_EXT_A_SUB1_START        0x1FA00
#define EMOJI_EXT_A_SUB1_END          0x1FA53
#define EMOJI_EXT_A_SUB2_START        0x1FA60
#define EMOJI_EXT_A_SUB2_END          0x1FA6D
#define EMOJI_EXT_A_SUB3_START        0x1FA70
#define EMOJI_EXT_A_SUB3_END          0x1FA7C
#define EMOJI_EXT_A_SUB4_START        0x1FA80
#define EMOJI_EXT_A_SUB4_END          0x1FA89
#define EMOJI_EXT_A_SUB5_START        0x1FA8F
#define EMOJI_EXT_A_SUB5_END          0x1FAC6
#define EMOJI_EXT_A_SUB6_START        0x1FACE
#define EMOJI_EXT_A_SUB6_END          0x1FADC
#define EMOJI_EXT_A_SUB7_START        0x1FADF
#define EMOJI_EXT_A_SUB7_END          0x1FAE9
#define EMOJI_EXT_A_SUB8_START        0x1FAF0
#define EMOJI_EXT_A_SUB8_END          0x1FAF8

/* Returns 1 if ch is a cherry-picked Miscellaneous Technical emoji. */
static inline int _PyUnicode_IsMiscTechnicalEmoji(Py_UCS4 ch)
{
    switch (ch) {
    case EMOJI_MISC_TECH_WATCH:
    case EMOJI_MISC_TECH_HOURGLASS:
    case EMOJI_MISC_TECH_FF:
    case EMOJI_MISC_TECH_REW:
    case EMOJI_MISC_TECH_UP:
    case EMOJI_MISC_TECH_DOWN:
    case EMOJI_MISC_TECH_ALARM:
    case EMOJI_MISC_TECH_HOURGLASS2:
        return 1;
    default:
        return 0;
    }
}

/* Returns 1 if ch is an assigned emoji codepoint.
   Uses precise sub-ranges to exclude unassigned codepoints (Cn)
   within blocks that have gaps. */
static inline int _PyUnicode_IsEmoji(Py_UCS4 ch)
{
    /* Cherry-picked Misc Technical characters */
    if (_PyUnicode_IsMiscTechnicalEmoji(ch)) return 1;
    /* Fully assigned BMP blocks */
    if (ch >= EMOJI_GEOMETRIC_SHAPES_START && ch <= EMOJI_GEOMETRIC_SHAPES_END) return 1;
    if (ch >= EMOJI_MISC_SYMBOLS_START && ch <= EMOJI_DINGBATS_END) return 1;
    /* Misc Symbols and Arrows — 3 sub-ranges */
    if (ch >= EMOJI_MSA_SUB1_START && ch <= EMOJI_MSA_SUB1_END) return 1;
    if (ch >= EMOJI_MSA_SUB2_START && ch <= EMOJI_MSA_SUB2_END) return 1;
    if (ch >= EMOJI_MSA_SUB3_START && ch <= EMOJI_MSA_SUB3_END) return 1;
    /* SMP — early exit for non-SMP */
    if (ch < EMOJI_REGIONAL_IND_START) return 0;
    /* Fully assigned SMP blocks */
    if (ch <= EMOJI_REGIONAL_IND_END) return 1;
    if (ch >= EMOJI_MISC_PICTOGRAPHS_START && ch <= EMOJI_MISC_PICTOGRAPHS_END) return 1;
    if (ch >= EMOJI_EMOTICONS_START && ch <= EMOJI_EMOTICONS_END) return 1;
    if (ch >= EMOJI_SUPPLEMENTAL_START && ch <= EMOJI_SUPPLEMENTAL_END) return 1;
    /* Transport and Map Symbols — 3 sub-ranges */
    if (ch >= EMOJI_TRANSPORT_SUB1_START && ch <= EMOJI_TRANSPORT_SUB1_END) return 1;
    if (ch >= EMOJI_TRANSPORT_SUB2_START && ch <= EMOJI_TRANSPORT_SUB2_END) return 1;
    if (ch >= EMOJI_TRANSPORT_SUB3_START && ch <= EMOJI_TRANSPORT_SUB3_END) return 1;
    /* Geometric Shapes Extended — 3 sub-ranges */
    if (ch >= EMOJI_GEO_EXT_SUB1_START && ch <= EMOJI_GEO_EXT_SUB1_END) return 1;
    if (ch >= EMOJI_GEO_EXT_SUB2_START && ch <= EMOJI_GEO_EXT_SUB2_END) return 1;
    if (ch == EMOJI_GEO_EXT_SUB3_START) return 1;  /* single char U+1F7F0 */
    /* Extended-A — 8 sub-ranges */
    if (ch >= EMOJI_EXT_A_SUB1_START && ch <= EMOJI_EXT_A_SUB1_END) return 1;
    if (ch >= EMOJI_EXT_A_SUB2_START && ch <= EMOJI_EXT_A_SUB2_END) return 1;
    if (ch >= EMOJI_EXT_A_SUB3_START && ch <= EMOJI_EXT_A_SUB3_END) return 1;
    if (ch >= EMOJI_EXT_A_SUB4_START && ch <= EMOJI_EXT_A_SUB4_END) return 1;
    if (ch >= EMOJI_EXT_A_SUB5_START && ch <= EMOJI_EXT_A_SUB5_END) return 1;
    if (ch >= EMOJI_EXT_A_SUB6_START && ch <= EMOJI_EXT_A_SUB6_END) return 1;
    if (ch >= EMOJI_EXT_A_SUB7_START && ch <= EMOJI_EXT_A_SUB7_END) return 1;
    if (ch >= EMOJI_EXT_A_SUB8_START && ch <= EMOJI_EXT_A_SUB8_END) return 1;
    return 0;
}

extern int _PyUnicode_IsXidStart(Py_UCS4 ch);
extern int _PyUnicode_IsXidContinue(Py_UCS4 ch);
extern int _PyUnicode_ToLowerFull(Py_UCS4 ch, Py_UCS4 *res);
extern int _PyUnicode_ToTitleFull(Py_UCS4 ch, Py_UCS4 *res);
extern int _PyUnicode_ToUpperFull(Py_UCS4 ch, Py_UCS4 *res);
extern int _PyUnicode_ToFoldedFull(Py_UCS4 ch, Py_UCS4 *res);
extern int _PyUnicode_IsCaseIgnorable(Py_UCS4 ch);
extern int _PyUnicode_IsCased(Py_UCS4 ch);

/* --- Unicode API -------------------------------------------------------- */

// Export for '_json' shared extension
PyAPI_FUNC(int) _PyUnicode_CheckConsistency(
    PyObject *op,
    int check_content);

PyAPI_FUNC(void) _PyUnicode_ExactDealloc(PyObject *op);
extern Py_ssize_t _PyUnicode_InternedSize(void);
extern Py_ssize_t _PyUnicode_InternedSize_Immortal(void);

// Get a copy of a Unicode string.
// Export for '_datetime' shared extension.
PyAPI_FUNC(PyObject*) _PyUnicode_Copy(
    PyObject *unicode);

/* Unsafe version of PyUnicode_Fill(): don't check arguments and so may crash
   if parameters are invalid (e.g. if length is longer than the string). */
extern void _PyUnicode_FastFill(
    PyObject *unicode,
    Py_ssize_t start,
    Py_ssize_t length,
    Py_UCS4 fill_char
    );

/* Unsafe version of PyUnicode_CopyCharacters(): don't check arguments and so
   may crash if parameters are invalid (e.g. if the output string
   is too short). */
extern void _PyUnicode_FastCopyCharacters(
    PyObject *to,
    Py_ssize_t to_start,
    PyObject *from,
    Py_ssize_t from_start,
    Py_ssize_t how_many
    );

/* Create a new string from a buffer of ASCII characters.
   WARNING: Don't check if the string contains any non-ASCII character. */
extern PyObject* _PyUnicode_FromASCII(
    const char *buffer,
    Py_ssize_t size);

/* Compute the maximum character of the substring unicode[start:end].
   Return 127 for an empty string. */
extern Py_UCS4 _PyUnicode_FindMaxChar (
    PyObject *unicode,
    Py_ssize_t start,
    Py_ssize_t end);

/* --- _PyUnicodeWriter API ----------------------------------------------- */

/* Format the object based on the format_spec, as defined in PEP 3101
   (Advanced String Formatting). */
extern int _PyUnicode_FormatAdvancedWriter(
    _PyUnicodeWriter *writer,
    PyObject *obj,
    PyObject *format_spec,
    Py_ssize_t start,
    Py_ssize_t end);

/* --- UTF-7 Codecs ------------------------------------------------------- */

extern PyObject* _PyUnicode_EncodeUTF7(
    PyObject *unicode,          /* Unicode object */
    int base64SetO,             /* Encode RFC2152 Set O characters in base64 */
    int base64WhiteSpace,       /* Encode whitespace (sp, ht, nl, cr) in base64 */
    const char *errors);        /* error handling */

/* --- UTF-8 Codecs ------------------------------------------------------- */

// Export for '_tkinter' shared extension.
PyAPI_FUNC(PyObject*) _PyUnicode_AsUTF8String(
    PyObject *unicode,
    const char *errors);

/* --- UTF-32 Codecs ------------------------------------------------------ */

// Export for '_tkinter' shared extension
PyAPI_FUNC(PyObject*) _PyUnicode_EncodeUTF32(
    PyObject *object,           /* Unicode object */
    const char *errors,         /* error handling */
    int byteorder);             /* byteorder to use 0=BOM+native;-1=LE,1=BE */

/* --- UTF-16 Codecs ------------------------------------------------------ */

// Returns a Python string object holding the UTF-16 encoded value of
// the Unicode data.
//
// If byteorder is not 0, output is written according to the following
// byte order:
//
// byteorder == -1: little endian
// byteorder == 0:  native byte order (writes a BOM mark)
// byteorder == 1:  big endian
//
// If byteorder is 0, the output string will always start with the
// Unicode BOM mark (U+FEFF). In the other two modes, no BOM mark is
// prepended.
//
// Export for '_tkinter' shared extension
PyAPI_FUNC(PyObject*) _PyUnicode_EncodeUTF16(
    PyObject* unicode,          /* Unicode object */
    const char *errors,         /* error handling */
    int byteorder);             /* byteorder to use 0=BOM+native;-1=LE,1=BE */

/* --- Unicode-Escape Codecs ---------------------------------------------- */

/* Variant of PyUnicode_DecodeUnicodeEscape that supports partial decoding. */
extern PyObject* _PyUnicode_DecodeUnicodeEscapeStateful(
    const char *string,     /* Unicode-Escape encoded string */
    Py_ssize_t length,      /* size of string */
    const char *errors,     /* error handling */
    Py_ssize_t *consumed);  /* bytes consumed */

// Helper for PyUnicode_DecodeUnicodeEscape that detects invalid escape
// chars.
// Export for test_peg_generator.
PyAPI_FUNC(PyObject*) _PyUnicode_DecodeUnicodeEscapeInternal2(
    const char *string,     /* Unicode-Escape encoded string */
    Py_ssize_t length,      /* size of string */
    const char *errors,     /* error handling */
    Py_ssize_t *consumed,   /* bytes consumed */
    int *first_invalid_escape_char, /* on return, if not -1, contain the first
                                       invalid escaped char (<= 0xff) or invalid
                                       octal escape (> 0xff) in string. */
    const char **first_invalid_escape_ptr); /* on return, if not NULL, may
                                        point to the first invalid escaped
                                        char in string.
                                        May be NULL if errors is not NULL. */

/* --- Raw-Unicode-Escape Codecs ---------------------------------------------- */

/* Variant of PyUnicode_DecodeRawUnicodeEscape that supports partial decoding. */
extern PyObject* _PyUnicode_DecodeRawUnicodeEscapeStateful(
    const char *string,     /* Unicode-Escape encoded string */
    Py_ssize_t length,      /* size of string */
    const char *errors,     /* error handling */
    Py_ssize_t *consumed);  /* bytes consumed */

/* --- Latin-1 Codecs ----------------------------------------------------- */

extern PyObject* _PyUnicode_AsLatin1String(
    PyObject* unicode,
    const char* errors);

/* --- ASCII Codecs ------------------------------------------------------- */

extern PyObject* _PyUnicode_AsASCIIString(
    PyObject* unicode,
    const char* errors);

/* --- Character Map Codecs ----------------------------------------------- */

/* Translate an Unicode object by applying a character mapping table to
   it and return the resulting Unicode object.

   The mapping table must map Unicode ordinal integers to Unicode strings,
   Unicode ordinal integers or None (causing deletion of the character).

   Mapping tables may be dictionaries or sequences. Unmapped character
   ordinals (ones which cause a LookupError) are left untouched and
   are copied as-is.
*/
extern PyObject* _PyUnicode_EncodeCharmap(
    PyObject *unicode,          /* Unicode object */
    PyObject *mapping,          /* encoding mapping */
    const char *errors);        /* error handling */

/* --- Decimal Encoder ---------------------------------------------------- */

// Converts a Unicode object holding a decimal value to an ASCII string
// for using in int, float and complex parsers.
// Transforms code points that have decimal digit property to the
// corresponding ASCII digit code points.  Transforms spaces to ASCII.
// Transforms code points starting from the first non-ASCII code point that
// is neither a decimal digit nor a space to the end into '?'.
//
// Export for '_testinternalcapi' shared extension.
PyAPI_FUNC(PyObject*) _PyUnicode_TransformDecimalAndSpaceToASCII(
    PyObject *unicode);         /* Unicode object */

/* --- Methods & Slots ---------------------------------------------------- */

PyAPI_FUNC(PyObject*) _PyUnicode_JoinArray(
    PyObject *separator,
    PyObject *const *items,
    Py_ssize_t seqlen
    );

/* Test whether a unicode is equal to ASCII identifier.  Return 1 if true,
   0 otherwise.  The right argument must be ASCII identifier.
   Any error occurs inside will be cleared before return. */
extern int _PyUnicode_EqualToASCIIId(
    PyObject *left,             /* Left string */
    _Py_Identifier *right       /* Right identifier */
    );

// Test whether a unicode is equal to ASCII string.  Return 1 if true,
// 0 otherwise.  The right argument must be ASCII-encoded string.
// Any error occurs inside will be cleared before return.
// Export for '_ctypes' shared extension
PyAPI_FUNC(int) _PyUnicode_EqualToASCIIString(
    PyObject *left,
    const char *right           /* ASCII-encoded string */
    );

/* Externally visible for str.strip(unicode) */
extern PyObject* _PyUnicode_XStrip(
    PyObject *self,
    int striptype,
    PyObject *sepobj
    );


/* Using explicit passed-in values, insert the thousands grouping
   into the string pointed to by buffer.  For the argument descriptions,
   see Objects/stringlib/localeutil.h */
extern Py_ssize_t _PyUnicode_InsertThousandsGrouping(
    _PyUnicodeWriter *writer,
    Py_ssize_t n_buffer,
    PyObject *digits,
    Py_ssize_t d_pos,
    Py_ssize_t n_digits,
    Py_ssize_t min_width,
    const char *grouping,
    PyObject *thousands_sep,
    Py_UCS4 *maxchar,
    int forward);

/* Dedent a string.
   Behaviour is expected to be an exact match of `textwrap.dedent`.
   Return a new reference on success, NULL with exception set on error.
   */
extern PyObject* _PyUnicode_Dedent(PyObject *unicode);

/* --- Misc functions ----------------------------------------------------- */

extern PyObject* _PyUnicode_FormatLong(PyObject *, int, int, int);

// Fast equality check when the inputs are known to be exact unicode types.
// Export for '_pickle' shared extension.
PyAPI_FUNC(int) _PyUnicode_Equal(PyObject *, PyObject *);

extern int _PyUnicode_WideCharString_Converter(PyObject *, void *);
extern int _PyUnicode_WideCharString_Opt_Converter(PyObject *, void *);

// Export for test_peg_generator
PyAPI_FUNC(Py_ssize_t) _PyUnicode_ScanIdentifier(PyObject *);

/* --- Runtime lifecycle -------------------------------------------------- */

extern void _PyUnicode_InitState(PyInterpreterState *);
extern PyStatus _PyUnicode_InitGlobalObjects(PyInterpreterState *);
extern PyStatus _PyUnicode_InitTypes(PyInterpreterState *);
extern void _PyUnicode_Fini(PyInterpreterState *);
extern void _PyUnicode_FiniTypes(PyInterpreterState *);

extern PyTypeObject _PyUnicodeASCIIIter_Type;

/* --- Interning ---------------------------------------------------------- */

// All these are "ref-neutral", like the public PyUnicode_InternInPlace.

// Explicit interning routines:
PyAPI_FUNC(void) _PyUnicode_InternMortal(PyInterpreterState *interp, PyObject **);
PyAPI_FUNC(void) _PyUnicode_InternImmortal(PyInterpreterState *interp, PyObject **);
// Left here to help backporting:
PyAPI_FUNC(void) _PyUnicode_InternInPlace(PyInterpreterState *interp, PyObject **p);
// Only for singletons in the _PyRuntime struct:
extern void _PyUnicode_InternStatic(PyInterpreterState *interp, PyObject **);

/* --- Other API ---------------------------------------------------------- */

extern void _PyUnicode_ClearInterned(PyInterpreterState *interp);

// Like PyUnicode_AsUTF8(), but check for embedded null characters.
// Export for '_sqlite3' shared extension.
PyAPI_FUNC(const char *) _PyUnicode_AsUTF8NoNUL(PyObject *);


#ifdef __cplusplus
}
#endif
#endif /* !Py_INTERNAL_UNICODEOBJECT_H */
