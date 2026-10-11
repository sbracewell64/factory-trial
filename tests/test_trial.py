import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout

from trial.__main__ import greeting, main


class GreetTests(unittest.TestCase):
    def test_greeting(self):
        self.assertEqual(greeting("Ada"), "Hello, Ada!")

    def test_greet_prints_the_greeting(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["greet", "Ada"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue(), "Hello, Ada!\n")

    def test_the_program_runs_as_a_module(self):
        r = subprocess.run([sys.executable, "-m", "trial", "greet", "Grace"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout, "Hello, Grace!\n")

    def test_greet_without_a_name_is_a_usage_error(self):
        r = subprocess.run([sys.executable, "-m", "trial", "greet"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("usage:", r.stderr)


if __name__ == "__main__":
    unittest.main()
