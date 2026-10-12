# Usage errors

A user who leaves something out or adds something trial does not know gets the usage line and one `error:` line on stderr, nothing on stdout, and exit code 2.

## Sub-features

- `usage-no-command` reports that `command` is required.
- `usage-no-name` reports that `name` is required for `greet`.
- `usage-unknown-command` reports an invalid choice and names `greet`.
- `usage-extra-args` reports unrecognized arguments.

## How to get to it (user POV)

- Run `python3 -m trial` with no arguments.
- Run `python3 -m trial greet` with no name.
- Run `python3 -m trial wave`.
- Run `python3 -m trial greet Ada Lovelace` without quotes.

## Driving it with verify.py

Preconditions:

- Launch printed `RUN=...` and `verify.py doctor --run <RUN>` exits 0.

- **No command.** Run `verify.py drive --run <RUN> usage-no-command --exit 2 --stdout '' --stderr-has 'trial: error: the following arguments are required: command' --`. Stderr starts with `usage: trial [-h] command ...`.
- **No name.** Run `verify.py drive --run <RUN> usage-no-name --exit 2 --stdout '' --stderr-has 'trial greet: error: the following arguments are required: name' -- greet`.
- **Unknown command.** Run `verify.py drive --run <RUN> usage-unknown-command --exit 2 --stdout '' --stderr-has "invalid choice: 'wave'" -- wave`.
- **Extra arguments.** Run `verify.py drive --run <RUN> usage-extra-args --exit 2 --stdout '' --stderr-has 'unrecognized arguments: Lovelace' -- greet Ada Lovelace`.

## Gotchas

- The no-command drive still needs the trailing `--` so verify.py passes no arguments to trial.
- `--stdout ''` is what proves stdout stayed empty; leave it in.
- The program name in errors is `trial`, not `__main__.py`, because the module sets `prog="trial"`.
