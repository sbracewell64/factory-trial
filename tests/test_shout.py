import subprocess
import sys
import unittest


def trial(*args):
    return subprocess.run([sys.executable, "-m", "trial", *args], capture_output=True, text=True)


class ShoutTests(unittest.TestCase):
    def test_greet_shout_prints_the_greeting_in_capitals(self):
        cases = {
            ("greet", "Ada", "--shout"): "HELLO, ADA!\n",
            ("greet", "--shout", "Ada Lovelace"): "HELLO, ADA LOVELACE!\n",
        }
        for args, expected in cases.items():
            with self.subTest(args=args):
                r = trial(*args)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(r.stdout, expected)
                self.assertEqual(r.stderr, "")

    def test_greet_without_shout_is_unchanged(self):
        r = trial("greet", "Ada")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "Hello, Ada!\n")

    def test_greet_help_lists_shout(self):
        r = trial("greet", "--help")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("--shout", r.stdout)
        self.assertIn("Print a greeting for NAME", r.stdout)


if __name__ == "__main__":
    unittest.main()
