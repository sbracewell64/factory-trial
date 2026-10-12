# Help text

A user asks trial or its `greet` command for help and reads the usage line, the description and the arguments on stdout, with exit code 0.

## Sub-features

- `help-root` shows the program usage and lists the `greet` command with `Print a greeting for NAME`.
- `help-greet` shows the `greet` usage, its description `Print a greeting for NAME` and its `name` argument (`who to greet`).

## How to get to it (user POV)

- Run `python3 -m trial --help` or `python3 -m trial -h`.
- Run `python3 -m trial greet --help` or `python3 -m trial greet -h`.

## Driving it with verify.py

Preconditions:

- Launch printed `RUN=...` and `verify.py doctor --run <RUN>` exits 0.

- **Program help.** Run `verify.py drive --run <RUN> help-root --exit 0 --stdout-has 'usage: trial [-h] command ...' --stdout-has 'Print a greeting for NAME' -- --help`. Stdout starts with `usage: trial [-h] command ...` and has the line `greet     Print a greeting for NAME`.
- **Short flag.** Run `verify.py drive --run <RUN> help-root-short --exit 0 --stdout-has 'usage: trial [-h] command ...' --stdout-has 'Print a greeting for NAME' -- -h`. The transcript matches `help-root`.
- **Command help.** Run `verify.py drive --run <RUN> help-greet --exit 0 --stdout-has 'usage: trial greet [-h] name' --stdout-has 'Print a greeting for NAME' --stdout-has 'who to greet' -- greet --help`. Stdout starts with `usage: trial greet [-h] name`, then the description `Print a greeting for NAME`, and has `name        who to greet`.
- **Command short flag.** Run `verify.py drive --run <RUN> help-greet-short --exit 0 --stdout-has 'usage: trial greet [-h] name' --stdout-has 'Print a greeting for NAME' --stdout-has 'who to greet' -- greet -h`. The transcript matches `help-greet`.

## Gotchas

- Help goes to stdout with exit 0; usage errors go to stderr with exit 2. Do not assert on stderr here.
- argparse wraps and aligns help text by terminal width and Python version. Assert the key lines with `--stdout-has`; do not assert the whole help text with `--stdout`.
- The unit test `test_help_describes_greet` checks that `--help` and `greet --help` print `Print a greeting for NAME` and no longer print `Say hello`. It does not check `-h` or the usage lines; this recipe does.
