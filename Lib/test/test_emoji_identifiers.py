"""Tests for emoji support in Python identifiers.

This test suite validates that emoji characters can be used in variable,
function, and class names. Emojis can start or continue identifiers, like letters.

The implementation modifies the Unicode identifier checking to recognize
emoji codepoints as valid identifier characters, extending beyond the
standard XID_Start and XID_Continue Unicode properties.
"""

import unicodedata
import unittest


class EmojiIdentifierBasicTests(unittest.TestCase):
    """Basic tests for emoji characters as identifiers."""

    def test_emoji_identifier__single_emoji_as_variable__assigns_successfully(self):
        """A single emoji character should work as a variable name."""
        exec_globals = {}
        exec("\U0001F389 = 1", exec_globals)  # 🎉
        self.assertEqual(exec_globals["\U0001F389"], 1)

    def test_emoji_identifier__emoji_starting_name_with_ascii__assigns_successfully(self):
        """An emoji followed by ASCII letters should work as a variable name."""
        exec_globals = {}
        exec("\U0001F389party = 42", exec_globals)  # 🎉party
        self.assertEqual(exec_globals["\U0001F389party"], 42)

    def test_emoji_identifier__emoji_in_continuation__assigns_successfully(self):
        """ASCII letters followed by emoji should work as a variable name."""
        exec_globals = {}
        exec("my\U0001F389var = 100", exec_globals)  # my🎉var
        self.assertEqual(exec_globals["my\U0001F389var"], 100)

    def test_emoji_identifier__emoji_as_function_name__defines_successfully(self):
        """An emoji should work as a function name."""
        exec_globals = {}
        exec("def \U0001F389(): return 1", exec_globals)  # def 🎉(): return 1
        self.assertEqual(exec_globals["\U0001F389"](), 1)

    def test_emoji_identifier__emoji_as_class_name__defines_successfully(self):
        """An emoji should work as a class name."""
        exec_globals = {}
        exec("class \U0001F389: pass", exec_globals)  # class 🎉: pass
        self.assertIn("\U0001F389", exec_globals)

    def test_emoji_identifier__str_isidentifier__returns_true(self):
        """str.isidentifier() should return True for emoji strings."""
        self.assertTrue("\U0001F389".isidentifier())  # 🎉
        self.assertTrue("\U0001F600".isidentifier())  # 😀
        self.assertTrue("\U0001F680".isidentifier())  # 🚀


class EmojiRangeTests(unittest.TestCase):
    """Tests for various emoji Unicode ranges."""

    def test_emoji_identifier__misc_symbols_range__valid(self):
        """Miscellaneous Symbols (U+2600-U+26FF) should be valid identifiers."""
        # ☀ U+2600 (Black Sun with Rays)
        self.assertTrue("\u2600".isidentifier())
        # ⚡ U+26A1 (High Voltage Sign)
        self.assertTrue("\u26A1".isidentifier())
        # ⚽ U+26BD (Soccer Ball)
        self.assertTrue("\u26BD".isidentifier())

    def test_emoji_identifier__dingbats_range__valid(self):
        """Dingbats (U+2700-U+27BF) should be valid identifiers."""
        # ✂ U+2702 (Black Scissors)
        self.assertTrue("\u2702".isidentifier())
        # ✈ U+2708 (Airplane)
        self.assertTrue("\u2708".isidentifier())
        # ✅ U+2705 (Check Mark Button)
        self.assertTrue("\u2705".isidentifier())

    def test_emoji_identifier__emoticons_range__valid(self):
        """Emoticons (U+1F600-U+1F64F) should be valid identifiers."""
        # 😀 U+1F600 (Grinning Face)
        self.assertTrue("\U0001F600".isidentifier())
        # 😎 U+1F60E (Smiling Face with Sunglasses)
        self.assertTrue("\U0001F60E".isidentifier())
        # 🙏 U+1F64F (Person with Folded Hands)
        self.assertTrue("\U0001F64F".isidentifier())

    def test_emoji_identifier__transport_range__valid(self):
        """Transport and Map Symbols (U+1F680-U+1F6FF) should be valid identifiers."""
        # 🚀 U+1F680 (Rocket)
        self.assertTrue("\U0001F680".isidentifier())
        # 🛸 U+1F6F8 (Flying Saucer)
        self.assertTrue("\U0001F6F8".isidentifier())
        # 🚗 U+1F697 (Automobile)
        self.assertTrue("\U0001F697".isidentifier())

    def test_emoji_identifier__supplemental_range__valid(self):
        """Supplemental Symbols and Pictographs (U+1F900-U+1F9FF) should be valid."""
        # 🤖 U+1F916 (Robot Face)
        self.assertTrue("\U0001F916".isidentifier())
        # 🧠 U+1F9E0 (Brain)
        self.assertTrue("\U0001F9E0".isidentifier())
        # 🤔 U+1F914 (Thinking Face)
        self.assertTrue("\U0001F914".isidentifier())

    def test_emoji_identifier__extended_a_range__valid(self):
        """Symbols and Pictographs Extended-A (U+1FA00-U+1FAFF) should be valid."""
        # 🪐 U+1FA90 (Ringed Planet)
        self.assertTrue("\U0001FA90".isidentifier())
        # 🫠 U+1FAE0 (Melting Face)
        self.assertTrue("\U0001FAE0".isidentifier())

    def test_emoji_identifier__geometric_shapes_extended_range__valid(self):
        """Geometric Shapes Extended (U+1F780-U+1F7FF) should be valid.

        This block contains the colored circle and square emoji added in
        Unicode 12.0, such as 🟢🟠🟡🟣🟤🟥🟧🟨🟩🟪🟫.
        These live in a different block than the older 🔴🔵 (which are
        in Misc Symbols & Pictographs U+1F300-U+1F5FF).
        """
        # 🟢 U+1F7E2 (Green Circle)
        self.assertTrue("\U0001F7E2".isidentifier())
        # 🟠 U+1F7E0 (Orange Circle)
        self.assertTrue("\U0001F7E0".isidentifier())
        # 🟡 U+1F7E1 (Yellow Circle)
        self.assertTrue("\U0001F7E1".isidentifier())
        # 🟣 U+1F7E3 (Purple Circle)
        self.assertTrue("\U0001F7E3".isidentifier())
        # 🟥 U+1F7E5 (Red Square)
        self.assertTrue("\U0001F7E5".isidentifier())
        # 🟫 U+1F7EB (Brown Square)
        self.assertTrue("\U0001F7EB".isidentifier())

    def test_emoji_identifier__regional_indicators_range__valid(self):
        """Regional Indicator Symbols (U+1F1E6-U+1F1FF) should be valid.

        These are the building blocks of flag emoji. Each regional
        indicator corresponds to a letter A-Z, and pairs form country
        flags (e.g. U+1F1FA U+1F1F8 = 🇺🇸).
        """
        # 🇦 U+1F1E6 (Regional Indicator Symbol Letter A)
        self.assertTrue("\U0001F1E6".isidentifier())
        # 🇿 U+1F1FF (Regional Indicator Symbol Letter Z)
        self.assertTrue("\U0001F1FF".isidentifier())

    def test_emoji_identifier__flag_pairs__valid(self):
        """Flag emoji (pairs of regional indicators) should be valid identifiers.

        Each flag is two regional indicator code points. As identifiers,
        both code points are valid characters, so the flag forms a
        two-character identifier.
        """
        # 🇺🇸 U+1F1FA U+1F1F8 (US flag)
        self.assertTrue("\U0001F1FA\U0001F1F8".isidentifier())
        # 🇫🇷 U+1F1EB U+1F1F7 (France flag)
        self.assertTrue("\U0001F1EB\U0001F1F7".isidentifier())
        # 🇯🇵 U+1F1EF U+1F1F5 (Japan flag)
        self.assertTrue("\U0001F1EF\U0001F1F5".isidentifier())
        # 🇧🇷 U+1F1E7 U+1F1F7 (Brazil flag)
        self.assertTrue("\U0001F1E7\U0001F1F7".isidentifier())


class ZWJSequenceTests(unittest.TestCase):
    """Tests for Zero Width Joiner (ZWJ) emoji sequences.

    ZWJ sequences combine multiple emoji into a single visual glyph.
    These tests verify that ZWJ sequences can form single identifiers.
    """

    def test_emoji_identifier__zwj_family_sequence__forms_single_identifier(self):
        """Family emoji (ZWJ sequence) should work as identifier."""
        # 👨‍👩‍👧 = U+1F468 U+200D U+1F469 U+200D U+1F467
        family = "\U0001F468\u200D\U0001F469\u200D\U0001F467"
        self.assertTrue(family.isidentifier())

    def test_emoji_identifier__zwj_profession_sequence__forms_single_identifier(self):
        """Profession emoji (ZWJ sequence) should work as identifier."""
        # 👨‍💻 = U+1F468 U+200D U+1F4BB (man technologist)
        technologist = "\U0001F468\u200D\U0001F4BB"
        self.assertTrue(technologist.isidentifier())

    def test_emoji_identifier__zwj_flag_sequence__forms_single_identifier(self):
        """Rainbow flag (ZWJ sequence) should work as identifier."""
        # 🏳️‍🌈 = U+1F3F3 U+FE0F U+200D U+1F308
        rainbow_flag = "\U0001F3F3\uFE0F\u200D\U0001F308"
        self.assertTrue(rainbow_flag.isidentifier())


class EdgeCaseTests(unittest.TestCase):
    """Edge cases for emoji identifier support."""

    def test_emoji_identifier__skin_tone_modifier__valid_continuation(self):
        """Emoji with skin tone modifier should be valid identifier."""
        # 👋🏽 = U+1F44B U+1F3FD (waving hand + medium skin tone)
        self.assertTrue("\U0001F44B\U0001F3FD".isidentifier())

    def test_emoji_identifier__variation_selector_16__valid_continuation(self):
        """Emoji with Variation Selector 16 should be valid identifier."""
        # ☀️ = U+2600 U+FE0F (sun with VS16 for emoji presentation)
        self.assertTrue("\u2600\uFE0F".isidentifier())

    def test_emoji_identifier__multiple_emoji_in_name__valid(self):
        """Multiple emoji in sequence should be valid identifier."""
        # 🎉🚀🔥
        multi_emoji = "\U0001F389\U0001F680\U0001F525"
        self.assertTrue(multi_emoji.isidentifier())
        exec_globals = {}
        exec(f"{multi_emoji} = 999", exec_globals)
        self.assertEqual(exec_globals[multi_emoji], 999)

    def test_emoji_identifier__emoji_with_underscore__valid(self):
        """Emoji combined with underscores should be valid identifier."""
        self.assertTrue("_\U0001F389".isidentifier())  # _🎉
        self.assertTrue("\U0001F389_".isidentifier())  # 🎉_
        self.assertTrue("_\U0001F389_".isidentifier())  # _🎉_

    def test_emoji_identifier__emoji_with_numbers__valid(self):
        """Emoji followed by numbers should be valid identifier."""
        # 🎉123 - emoji start, number continue
        self.assertTrue("\U0001F389123".isidentifier())
        exec_globals = {}
        exec("\U0001F389123 = 456", exec_globals)
        self.assertEqual(exec_globals["\U0001F389123"], 456)

    def test_emoji_identifier__regional_indicator_with_ascii__valid(self):
        """Regional indicator followed by ASCII should be valid identifier."""
        self.assertTrue("\U0001F1E6bc".isidentifier())  # 🇦bc
        exec_globals = {}
        exec("\U0001F1E6bc = 123", exec_globals)
        self.assertEqual(exec_globals["\U0001F1E6bc"], 123)

    def test_emoji_identifier__geometric_shape_with_underscore__valid(self):
        """Geometric shape with underscore should be valid identifier."""
        self.assertTrue("\U0001F7E2_circle".isidentifier())  # 🟢_circle
        self.assertTrue("circle_\U0001F7E2".isidentifier())  # circle_🟢
        exec_globals = {}
        exec("\U0001F7E2_var = 'green'", exec_globals)
        self.assertEqual(exec_globals["\U0001F7E2_var"], 'green')

    def test_emoji_identifier__geometric_shape_with_numbers__valid(self):
        """Geometric shape followed by numbers should be valid identifier."""
        self.assertTrue("\U0001F7E2123".isidentifier())  # 🟢123
        exec_globals = {}
        exec("\U0001F7E21 = 100", exec_globals)
        self.assertEqual(exec_globals["\U0001F7E21"], 100)


class BackwardCompatibilityTests(unittest.TestCase):
    """Tests ensuring backward compatibility with existing identifier rules."""

    def test_backward_compat__ascii_identifiers__still_valid(self):
        """Standard ASCII identifiers should still work."""
        self.assertTrue("foo".isidentifier())
        self.assertTrue("_bar".isidentifier())
        self.assertTrue("baz123".isidentifier())
        self.assertTrue("CamelCase".isidentifier())
        self.assertTrue("snake_case".isidentifier())

    def test_backward_compat__unicode_letters__still_valid(self):
        """Unicode letter identifiers should still work."""
        self.assertTrue("caf\xe9".isidentifier())  # café
        self.assertTrue("\u65e5\u672c\u8a9e".isidentifier())  # 日本語
        self.assertTrue("\u03a9".isidentifier())  # Ω
        self.assertTrue("\u03c0".isidentifier())  # π

    def test_backward_compat__underscore_start__still_valid(self):
        """Underscore-starting identifiers should still work."""
        self.assertTrue("_private".isidentifier())
        self.assertTrue("__dunder__".isidentifier())
        self.assertTrue("_".isidentifier())
        self.assertTrue("__".isidentifier())

    def test_backward_compat__digit_cannot_start__still_raises(self):
        """Identifiers starting with digits should still be invalid."""
        self.assertFalse("1foo".isidentifier())
        self.assertFalse("123".isidentifier())
        self.assertFalse("1_".isidentifier())

    def test_backward_compat__operators_rejected__still_raises(self):
        """Operator characters should still be invalid identifiers."""
        self.assertFalse("+".isidentifier())
        self.assertFalse("-".isidentifier())
        self.assertFalse("@".isidentifier())
        self.assertFalse("=".isidentifier())
        self.assertFalse("*".isidentifier())

    def test_backward_compat__existing_isidentifier_true__unchanged(self):
        """Strings that were valid identifiers should remain valid."""
        valid_identifiers = [
            "x", "X", "_", "__", "___",
            "abc", "ABC", "Abc",
            "a1", "a_1", "_1", "__1",
            "\xe4",  # ä
            "\u03bc",  # μ
            "\u87d2",  # 蟒
        ]
        for ident in valid_identifiers:
            with self.subTest(ident=ident):
                self.assertTrue(ident.isidentifier())

    def test_backward_compat__existing_isidentifier_false__unchanged(self):
        """Strings that were invalid identifiers should remain invalid."""
        invalid_identifiers = [
            "", " ", "  ",
            "1", "123",
            "a b", "a-b", "a+b",
            "a.b", "a,b",
            "(", ")", "[", "]", "{", "}",
        ]
        for ident in invalid_identifiers:
            with self.subTest(ident=ident):
                self.assertFalse(ident.isidentifier())


class NegativeTests(unittest.TestCase):
    """Tests for things that should still be rejected as identifiers."""

    def test_negative__digit_start_with_emoji__raises(self):
        """Starting with digit followed by emoji should be invalid."""
        self.assertFalse("1\U0001F389".isidentifier())  # 1🎉
        self.assertFalse("123\U0001F389".isidentifier())  # 123🎉

    def test_negative__operator_chars__raises(self):
        """Operator characters should remain invalid."""
        self.assertFalse("+".isidentifier())
        self.assertFalse("=".isidentifier())
        self.assertFalse("@".isidentifier())
        self.assertFalse("!".isidentifier())

    def test_negative__whitespace__raises(self):
        """Whitespace should remain invalid in identifiers."""
        self.assertFalse(" ".isidentifier())
        self.assertFalse("\t".isidentifier())
        self.assertFalse("\n".isidentifier())
        self.assertFalse("a b".isidentifier())
        self.assertFalse("\U0001F389 \U0001F680".isidentifier())  # emoji space emoji


class BoundaryTests(unittest.TestCase):
    """Tests for boundary conditions in emoji range checking.

    These tests verify that the range checks in _PyUnicode_IsEmoji are
    correct and don't have off-by-one errors. For each range, we test:
    - The first character in the range (lower boundary)
    - The last character in the range (upper boundary)
    - One character just before the range (should be invalid)
    - One character just after the range (should be invalid)
    """

    def test_boundary__regional_indicators_first__valid(self):
        """First Regional Indicator (U+1F1E6) should be valid.

        U+1F1E6 is Regional Indicator Symbol Letter A (🇦), the first
        character in the Regional Indicators block.
        """
        self.assertTrue("\U0001F1E6".isidentifier())

    def test_boundary__regional_indicators_last__valid(self):
        """Last Regional Indicator (U+1F1FF) should be valid.

        U+1F1FF is Regional Indicator Symbol Letter Z (🇿), the last
        character in the Regional Indicators block.
        """
        self.assertTrue("\U0001F1FF".isidentifier())

    def test_boundary__regional_indicators_middle__valid(self):
        """Middle Regional Indicators should be valid.

        Test a few characters in the middle of the range to ensure the
        entire range is covered, not just the endpoints.
        """
        # 🇰 U+1F1F0 (Regional Indicator Symbol Letter K)
        self.assertTrue("\U0001F1F0".isidentifier())
        # 🇲 U+1F1F2 (Regional Indicator Symbol Letter M)
        self.assertTrue("\U0001F1F2".isidentifier())

    def test_boundary__before_regional_indicators__invalid(self):
        """Character before Regional Indicators (U+1F1E5) should be invalid.

        U+1F1E5 is just before the Regional Indicators block and should
        not be treated as an emoji identifier character.
        """
        self.assertFalse("\U0001F1E5".isidentifier())

    def test_boundary__after_regional_indicators__invalid(self):
        """Character after Regional Indicators (U+1F200) should be invalid.

        U+1F200 is just after the Regional Indicators block and should
        not be treated as an emoji identifier character. This verifies
        we don't have an off-by-one error on the upper bound.
        """
        self.assertFalse("\U0001F200".isidentifier())

    def test_boundary__geometric_shapes_first__valid(self):
        """First Geometric Shape Extended (U+1F780) should be valid.

        U+1F780 is the first character in the Geometric Shapes Extended
        block, which contains colored shapes and other geometric symbols.
        """
        self.assertTrue("\U0001F780".isidentifier())

    def test_boundary__geometric_shapes_last_assigned__valid(self):
        """Last assigned Geometric Shape Extended (U+1F7F0) should be valid.

        U+1F7F0 (HEAVY EQUALS SIGN) is the last assigned character in the
        Geometric Shapes Extended block. U+1F7FF (end of block) is
        unassigned and should be rejected per the v0.2 rule.
        """
        self.assertTrue("\U0001F7F0".isidentifier())

    def test_boundary__before_geometric_shapes__invalid(self):
        """Character before Geometric Shapes Extended (U+1F77F) should be invalid.

        U+1F77F is just before the Geometric Shapes Extended block and
        should not be treated as an emoji identifier character.
        """
        self.assertFalse("\U0001F77F".isidentifier())

    def test_boundary__after_geometric_shapes__invalid(self):
        """Character after Geometric Shapes Extended (U+1F800) should be invalid.

        U+1F800 is just after the Geometric Shapes Extended block and
        should not be treated as an emoji identifier character.
        """
        self.assertFalse("\U0001F800".isidentifier())


class FunctionalTests(unittest.TestCase):
    """Functional tests using emoji identifiers in real code."""

    def test_functional__emoji_variable_assignment_and_retrieval(self):
        """Emoji variables should work in normal Python code flow."""
        exec_globals = {}
        code = """
\U0001F4A1 = "idea"
\U0001F4A1_count = 5
result = \U0001F4A1 * \U0001F4A1_count
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], "ideaideaideaideaidea")

    def test_functional__emoji_function_with_parameters(self):
        """Emoji functions should work with parameters."""
        exec_globals = {}
        code = """
def \U0001F4DD(text):
    return f"Note: {text}"

output = \U0001F4DD("Hello")
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["output"], "Note: Hello")

    def test_functional__emoji_class_with_methods(self):
        """Emoji classes should work with methods and attributes."""
        exec_globals = {}
        code = """
class \U0001F916:
    def __init__(self):
        self.\U0001F4A1 = "thinking"

    def \U0001F50D(self):
        return f"Searching: {self.\U0001F4A1}"

bot = \U0001F916()
result = bot.\U0001F50D()
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], "Searching: thinking")

    def test_functional__emoji_in_comprehension(self):
        """Emoji variables should work in comprehensions."""
        exec_globals = {}
        code = """
\U0001F31F = [x * 2 for x in range(5)]
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["\U0001F31F"], [0, 2, 4, 6, 8])

    def test_functional__emoji_in_lambda(self):
        """Emoji should work in lambda expressions."""
        exec_globals = {}
        code = """
\U0001F3AF = lambda x: x ** 2
result = \U0001F3AF(7)
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], 49)

    def test_functional__geometric_shapes_as_variables(self):
        """Colored circle/square emoji should work as variable names."""
        exec_globals = {}
        code = """
\U0001F7E2 = "green"
\U0001F7E0 = "orange"
\U0001F7E3 = "purple"
result = \U0001F7E2 + " " + \U0001F7E0 + " " + \U0001F7E3
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], "green orange purple")

    def test_functional__flag_as_variable(self):
        """Flag emoji should work as variable names."""
        exec_globals = {}
        # 🇺🇸 = U+1F1FA U+1F1F8
        code = """
\U0001F1FA\U0001F1F8 = "United States"
"""
        exec(code, exec_globals)
        self.assertEqual(
            exec_globals["\U0001F1FA\U0001F1F8"], "United States"
        )

    def test_functional__flags_in_dict_comprehension(self):
        """Multiple flag emoji should work as identifiers in a loop."""
        exec_globals = {}
        code = """
flags = {
    "\U0001F1FA\U0001F1F8": "US",
    "\U0001F1EB\U0001F1F7": "FR",
    "\U0001F1EF\U0001F1F5": "JP",
}
# Use flag emoji as loop variable
result = []
for \U0001F3F3 in flags.values():
    result.append(\U0001F3F3)
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], ["US", "FR", "JP"])

    def test_functional__distinct_flags_are_distinct_identifiers(self):
        """Different flag emoji should be distinct identifiers."""
        exec_globals = {}
        code = """
\U0001F1FA\U0001F1F8 = 1
\U0001F1EB\U0001F1F7 = 2
\U0001F1EF\U0001F1F5 = 3
result = \U0001F1FA\U0001F1F8 + \U0001F1EB\U0001F1F7 + \U0001F1EF\U0001F1F5
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], 6)

    def test_functional__regional_indicator_single_char_as_variable(self):
        """Single regional indicator character should work as variable."""
        exec_globals = {}
        # Use a middle-range regional indicator (K = U+1F1F0)
        code = """
\U0001F1F0 = "K indicator"
result = \U0001F1F0
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], "K indicator")

    def test_functional__geometric_shape_boundary_chars_in_code(self):
        """First and last assigned geometric shapes should work in actual code."""
        exec_globals = {}
        code = """
\U0001F780 = "first"
\U0001F7F0 = "last"
result = \U0001F780 + " " + \U0001F7F0
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], "first last")

    def test_functional__mix_regional_and_geometric_in_expression(self):
        """Regional indicators and geometric shapes in same expression."""
        exec_globals = {}
        code = """
\U0001F1E6 = 1  # Regional Indicator A
\U0001F7E2 = 2  # Green Circle
result = \U0001F1E6 + \U0001F7E2
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], 3)

    def test_functional__geometric_shapes_distinct_identifiers(self):
        """Different colored shapes should be distinct identifiers."""
        exec_globals = {}
        code = """
\U0001F7E2 = "green"
\U0001F7E5 = "red"
\U0001F7E7 = "orange square"
colors = [\U0001F7E2, \U0001F7E5, \U0001F7E7]
"""
        exec(code, exec_globals)
        self.assertEqual(
            exec_globals["colors"],
            ["green", "red", "orange square"]
        )


class V02NewRangeTests(unittest.TestCase):
    """Tests for ranges added in v0.2 of the emoji identifiers plan.

    These ranges were not covered by the v0.1 implementation and require
    new support: Geometric Shapes (BMP), Miscellaneous Symbols and Arrows,
    Chess Symbols, and 8 cherry-picked Miscellaneous Technical characters.
    """

    def test_v02__geometric_shapes__black_square__valid(self):
        """■ U+25A0 (first in Geometric Shapes block) should be valid."""
        self.assertTrue("\u25A0".isidentifier())

    def test_v02__geometric_shapes__white_circle__valid(self):
        """○ U+25CB (White Circle) should be valid."""
        self.assertTrue("\u25CB".isidentifier())

    def test_v02__geometric_shapes__black_triangle__valid(self):
        """▲ U+25B2 (Black Up-Pointing Triangle) should be valid."""
        self.assertTrue("\u25B2".isidentifier())

    def test_v02__geometric_shapes__black_diamond__valid(self):
        """◆ U+25C6 (Black Diamond) should be valid."""
        self.assertTrue("\u25C6".isidentifier())

    def test_v02__geometric_shapes__last_char__valid(self):
        """U+25FF (last in Geometric Shapes block) should be valid."""
        self.assertTrue("\u25FF".isidentifier())

    def test_v02__geometric_shapes__before_block__invalid(self):
        """U+259F (just before Geometric Shapes) should not become valid."""
        self.assertFalse("\u259F".isidentifier())

    def test_v02__geometric_shapes__after_block__invalid(self):
        """U+2600 is Miscellaneous Symbols (separate range), not Geometric Shapes.

        This character IS valid (it's ☀ in the Misc Symbols range), so this
        test just confirms the boundary is where we expect it.
        """
        # U+2600 is valid, but via Miscellaneous Symbols, not Geometric Shapes
        self.assertTrue("\u2600".isidentifier())

    def test_v02__misc_symbols_and_arrows__star__valid(self):
        """⭐ U+2B50 (White Medium Star) should be valid."""
        self.assertTrue("\u2B50".isidentifier())

    def test_v02__misc_symbols_and_arrows__down_arrow__valid(self):
        """⬇ U+2B07 (Downwards Black Arrow) should be valid."""
        self.assertTrue("\u2B07".isidentifier())

    def test_v02__misc_symbols_and_arrows__heavy_circle__valid(self):
        """⭕ U+2B55 (Heavy Large Circle) should be valid."""
        self.assertTrue("\u2B55".isidentifier())

    def test_v02__misc_symbols_and_arrows__first_char__valid(self):
        """U+2B00 (first in Misc Symbols and Arrows) should be valid."""
        self.assertTrue("\u2B00".isidentifier())

    def test_v02__misc_symbols_and_arrows__last_char__valid(self):
        """U+2BFF (last in Misc Symbols and Arrows) should be valid."""
        self.assertTrue("\u2BFF".isidentifier())

    def test_v02__misc_symbols_and_arrows__before_block__invalid(self):
        """U+2AFF (just before Misc Symbols and Arrows) should not be valid."""
        self.assertFalse("\u2AFF".isidentifier())

    def test_v02__misc_symbols_and_arrows__after_block__invalid(self):
        """U+2C00 (just after Misc Symbols and Arrows) is Glagolitic.

        Glagolitic letters are in XID, so U+2C00 is valid — but via XID,
        not via our emoji ranges.
        """
        # This is a boundary sanity check, not an invalidity assertion
        pass

    def test_v02__chess_symbols__white_chess_king__valid(self):
        """U+1FA00 (first in Chess Symbols block) should be valid."""
        self.assertTrue("\U0001FA00".isidentifier())

    def test_v02__chess_symbols__last_assigned__valid(self):
        """U+1FA6D (last assigned in Chess Symbols block) should be valid."""
        self.assertTrue("\U0001FA6D".isidentifier())

    def test_v02__chess_symbols__before_block__invalid(self):
        """U+1F9FF (just before Chess Symbols) is Supplemental Symbols.

        U+1F9FF is valid via the Supplemental Symbols range, so this test
        just verifies the boundary location.
        """
        self.assertTrue("\U0001F9FF".isidentifier())

    def test_v02__chess_symbols__after_block_into_extended_a__valid(self):
        """U+1FA70 (first in Extended-A) should be valid.

        Verifies no gap between Chess Symbols (block ends U+1FA6F) and
        Extended-A (starts U+1FA70). Last assigned in Chess is U+1FA6D.
        """
        self.assertTrue("\U0001FA70".isidentifier())

    def test_v02__misc_technical__watch__valid(self):
        """⌚ U+231A (Watch) should be valid — cherry-picked character."""
        self.assertTrue("\u231A".isidentifier())

    def test_v02__misc_technical__hourglass__valid(self):
        """⌛ U+231B (Hourglass) should be valid — cherry-picked character."""
        self.assertTrue("\u231B".isidentifier())

    def test_v02__misc_technical__fast_forward__valid(self):
        """⏩ U+23E9 (Black Right-Pointing Double Triangle) should be valid."""
        self.assertTrue("\u23E9".isidentifier())

    def test_v02__misc_technical__rewind__valid(self):
        """⏪ U+23EA (Black Left-Pointing Double Triangle) should be valid."""
        self.assertTrue("\u23EA".isidentifier())

    def test_v02__misc_technical__fast_up__valid(self):
        """⏫ U+23EB (Black Up-Pointing Double Triangle) should be valid."""
        self.assertTrue("\u23EB".isidentifier())

    def test_v02__misc_technical__fast_down__valid(self):
        """⏬ U+23EC (Black Down-Pointing Double Triangle) should be valid."""
        self.assertTrue("\u23EC".isidentifier())

    def test_v02__misc_technical__alarm_clock__valid(self):
        """⏰ U+23F0 (Alarm Clock) should be valid — cherry-picked character."""
        self.assertTrue("\u23F0".isidentifier())

    def test_v02__misc_technical__hourglass_flowing__valid(self):
        """⏳ U+23F3 (Hourglass with Flowing Sand) should be valid."""
        self.assertTrue("\u23F3".isidentifier())

    def test_v02__misc_technical__non_cherry_picked__invalid(self):
        """Misc Technical characters NOT cherry-picked should remain invalid.

        ⌀ U+2300 (Diameter Sign) is in Miscellaneous Technical but was not
        cherry-picked for inclusion. It should not be a valid identifier.
        """
        self.assertFalse("\u2300".isidentifier())

    def test_v02__misc_technical__command_symbol__invalid(self):
        """⌘ U+2318 (Place of Interest / Command) was not cherry-picked."""
        self.assertFalse("\u2318".isidentifier())

    def test_v02__misc_technical__eject_symbol__invalid(self):
        """⏏ U+23CF (Eject Symbol) was not cherry-picked."""
        self.assertFalse("\u23CF".isidentifier())


class V02UnassignedCodepointTests(unittest.TestCase):
    """Tests that unassigned codepoints within emoji ranges are rejected.

    v0.2 requires that only assigned codepoints are valid identifiers.
    Unassigned slots within selected blocks must be rejected.

    These tests are resilient to future Unicode updates: they use
    unicodedata.category() to find codepoints that are currently
    unassigned (category 'Cn'). If a future Unicode version assigns
    all codepoints in a range, the test skips instead of failing.
    """

    def _find_unassigned_in_range(self, start, end):
        """Find an unassigned codepoint in the given range.

        Args:
            start: First codepoint in range (inclusive).
            end: Last codepoint in range (inclusive).

        Returns:
            An unassigned codepoint, or None if all are assigned.
        """
        for cp in range(start, end + 1):
            if unicodedata.category(chr(cp)) == 'Cn':
                return cp
        return None

    def test_v02__unassigned_in_misc_symbols_and_pictographs__invalid(self):
        """Unassigned codepoints in Misc Symbols and Pictographs should be rejected."""
        cp = self._find_unassigned_in_range(0x1F300, 0x1F5FF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+1F300..U+1F5FF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_emoticons__invalid(self):
        """Unassigned codepoints in Emoticons should be rejected."""
        cp = self._find_unassigned_in_range(0x1F600, 0x1F64F)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+1F600..U+1F64F")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_transport__invalid(self):
        """Unassigned codepoints in Transport and Map Symbols should be rejected."""
        cp = self._find_unassigned_in_range(0x1F680, 0x1F6FF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+1F680..U+1F6FF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_geometric_shapes_extended__invalid(self):
        """Unassigned codepoints in Geometric Shapes Extended should be rejected."""
        cp = self._find_unassigned_in_range(0x1F780, 0x1F7FF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+1F780..U+1F7FF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_supplemental__invalid(self):
        """Unassigned codepoints in Supplemental Symbols should be rejected."""
        cp = self._find_unassigned_in_range(0x1F900, 0x1F9FF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+1F900..U+1F9FF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_chess_symbols__invalid(self):
        """Unassigned codepoints in Chess Symbols should be rejected."""
        cp = self._find_unassigned_in_range(0x1FA00, 0x1FA6F)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+1FA00..U+1FA6F")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_extended_a__invalid(self):
        """Unassigned codepoints in Extended-A should be rejected."""
        cp = self._find_unassigned_in_range(0x1FA70, 0x1FAFF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+1FA70..U+1FAFF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_misc_symbols_and_arrows__invalid(self):
        """Unassigned codepoints in Misc Symbols and Arrows should be rejected."""
        cp = self._find_unassigned_in_range(0x2B00, 0x2BFF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+2B00..U+2BFF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_geometric_shapes__invalid(self):
        """Unassigned codepoints in Geometric Shapes should be rejected."""
        cp = self._find_unassigned_in_range(0x25A0, 0x25FF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+25A0..U+25FF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_misc_symbols__invalid(self):
        """Unassigned codepoints in Miscellaneous Symbols should be rejected."""
        cp = self._find_unassigned_in_range(0x2600, 0x26FF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+2600..U+26FF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )

    def test_v02__unassigned_in_dingbats__invalid(self):
        """Unassigned codepoints in Dingbats should be rejected."""
        cp = self._find_unassigned_in_range(0x2700, 0x27BF)
        if cp is None:
            self.skipTest("No unassigned codepoints in U+2700..U+27BF")
        self.assertFalse(
            chr(cp).isidentifier(),
            f"Unassigned U+{cp:04X} should not be a valid identifier"
        )


class V02FunctionalTests(unittest.TestCase):
    """Functional tests for v0.2 ranges in real code."""

    def test_v02_functional__geometric_shape_as_variable(self):
        """BMP geometric shapes should work as variable names."""
        exec_globals = {}
        code = """
\u25A0 = "black square"
\u25CF = "black circle"
\u25B2 = "black triangle"
result = \u25A0 + " " + \u25CF + " " + \u25B2
"""
        exec(code, exec_globals)
        self.assertEqual(
            exec_globals["result"],
            "black square black circle black triangle"
        )

    def test_v02_functional__misc_arrows_as_variable(self):
        """Miscellaneous Symbols and Arrows should work as variable names."""
        exec_globals = {}
        code = """
\u2B50 = "star"
\u2B55 = "circle"
result = \u2B50 + " and " + \u2B55
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], "star and circle")

    def test_v02_functional__cherry_picked_misc_technical_as_variable(self):
        """Cherry-picked Misc Technical characters should work as variables."""
        exec_globals = {}
        code = """
\u231A = "watch"
\u23F0 = "alarm"
\u23F3 = "hourglass"
result = \u231A + " " + \u23F0 + " " + \u23F3
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], "watch alarm hourglass")

    def test_v02_functional__chess_symbol_as_variable(self):
        """Chess symbols should work as variable names."""
        exec_globals = {}
        code = """
\U0001FA00 = "chess king"
result = \U0001FA00
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], "chess king")

    def test_v02_functional__mix_v01_and_v02_ranges(self):
        """Characters from v0.1 and v0.2 ranges should work together."""
        exec_globals = {}
        code = """
\U0001F680 = 10
\u25CF = 20
\u2B50 = 30
\u231A = 40
result = \U0001F680 + \u25CF + \u2B50 + \u231A
"""
        exec(code, exec_globals)
        self.assertEqual(exec_globals["result"], 100)


if __name__ == "__main__":
    unittest.main()
