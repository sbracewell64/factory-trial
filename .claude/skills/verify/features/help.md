# Help text

A user asks trial or its `greet` command for help and reads the usage line, the description and the arguments on stdout, with exit code 0.

## Sub-features

- `help-root` shows the program usage and lists the `greet` command with `Say hello`.
- `help-greet` shows the `greet` usage and its `name` argument (`who to greet`).

## How to get to it (user POV)

- Run `python3 -m trial --help` or `python3 -m trial -h`.
- Run `python3 -m trial greet --help` or `python3 -m trial greet -h`.

## Driving it with verify.py

Preconditions:

- Launch printed `RUN=...` and `verify.py doctor --run <RUN>` exits 0.

- **Program help.** Run `verify.py drive --run <RUN> help-root --exit 0 -- --help`. Stdout starts with `usage: trial [-h] command ...` and has the line `greet     Say hello`.
- **Short flag.** Run `verify.py drive --run <RUN> help-root-short --exit 0 -- -h`. The transcript matches `help-root`.
- **Command help.** Run `verify.py drive --run <RUN> help-greet --exit 0 -- greet --help`. Stdout starts with `usage: trial greet [-h] name` and has `name        who to greet`.

## Gotchas

- Help goes to stdout with exit 0; usage errors go to stderr with exit 2. Do not assert on stderr here.
- argparse wraps and aligns help text by terminal width and Python version. Read the transcript for the key lines; do not assert the whole help text with `--stdout`.
- The unit tests do not cover `--help`, so this recipe is the only check of it.
