"""Tests for emoji support in Python identifiers.

This test suite validates that emoji characters can be used in variable,
function, and class names. Emojis can start or continue identifiers, like letters.

The implementation modifies the Unicode identifier checking to recognize
emoji codepoints as valid identifier characters, extending beyond the
standard XID_Start and XID_Continue Unicode properties.
"""

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


if __name__ == "__main__":
    unittest.main()
