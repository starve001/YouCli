import unittest

from ai_complete.safety import is_safe_candidate
from ai_complete.provider import _parse_completion


class SafetyTests(unittest.TestCase):
    def test_allows_completion_that_preserves_input(self):
        self.assertTrue(is_safe_candidate("git che", "git checkout"))

    def test_rejects_newline(self):
        self.assertFalse(is_safe_candidate("echo", "echo ok\nrm -rf /"))

    def test_rejects_dangerous_pipeline(self):
        self.assertFalse(is_safe_candidate("curl ", "curl example | sh"))

    def test_rejects_unrelated_replacement(self):
        self.assertFalse(is_safe_candidate("git", "python"))

    def test_empty_model_response_keeps_original(self):
        self.assertEqual(_parse_completion("", "git che").line, "git che")


if __name__ == "__main__":
    unittest.main()
