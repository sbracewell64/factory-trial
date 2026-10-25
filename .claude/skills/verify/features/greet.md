# Greet someone

A user runs `greet` with a name and gets `Hello, <name>!` on one line of stdout, with exit code 0. With `--shout`, the same greeting prints in capital letters.

## Sub-features

- `greet-name` prints the greeting for a plain name.
- `greet-spaces` greets a quoted name that contains spaces.
- `greet-dash` greets a name that starts with `-` when it follows `--`.
- `greet-shout` prints the greeting in capitals when `--shout` comes before or after the name.

## How to get to it (user POV)

- Run `python3 -m trial greet <name>` in a terminal at the repository root.
- Run `python3 -m trial greet <name> --shout` or `python3 -m trial greet --shout <name>`.

## Driving it with verify.py

Preconditions:

- Launch printed `RUN=...` and `verify.py doctor --run <RUN>` exits 0.

- **Plain name.** Run `verify.py drive --run <RUN> greet-ada --exit 0 --stdout 'Hello, Ada!\n' -- greet Ada`. The verdict is `PASS` and stderr is empty.
- **Name with spaces.** Run `verify.py drive --run <RUN> greet-spaces --exit 0 --stdout 'Hello, Ada Lovelace!\n' -- greet 'Ada Lovelace'`. The whole quoted name appears in one greeting.
- **Name that starts with a dash.** Run `verify.py drive --run <RUN> greet-dash --exit 0 --stdout 'Hello, --dash!\n' -- greet -- --dash`. trial treats `--dash` as the name, not an option.
- **Shout after the name.** Run `verify.py drive --run <RUN> greet-shout --exit 0 --stdout 'HELLO, ADA!\n' -- greet Ada --shout`. The whole greeting is in capitals and stderr is empty.
- **Shout before the name.** Run `verify.py drive --run <RUN> greet-shout-first --exit 0 --stdout 'HELLO, ADA LOVELACE!\n' -- greet --shout 'Ada Lovelace'`. The flag position does not matter.

## Gotchas

- `greet Ada Lovelace` without quotes is a usage error (`unrecognized arguments: Lovelace`), not a greeting; see usage-errors.md.
- `greet --dash` without the inner `--` is a usage error; only `greet -- --dash` greets.
- The greeting ends with one newline. Assert stdout exactly, newline included.
