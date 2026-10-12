# trial verification map

This directory is the maintained source for verifying what a user of trial can see. Read this index, then use the matching feature file as the recipe.

## Baseline preconditions

- Work from the repository root with `python3` (3.12 or later) on `PATH`. trial has no dependencies.
- Launch, then require `verify.py doctor --run <RUN>` to exit 0.
- Drive only the checkout Launch recorded.

## Driving conventions

- `verify.py` in every recipe means `python3 .claude/skills/verify/scripts/verify.py`, run from the repository root.
- Every drive is `verify.py drive --run <RUN> <label> [assertions] -- <trial args>` (see SKILL.md, Drive).
- Use the feature's sub-feature ID as the label prefix (`greet-ada`, `help-root`).
- Copy names, flags and expected text literally.

## Proof and skip reporting

- CLI proof is the transcript: command, exit code, stdout, stderr and verdict.
- Record the feature file and entry point with every transcript.
- Report an entry point you could not drive with the command you tried and the unmet precondition. Never count a different entry point as the skipped one.

## Features

- [Greet someone](./greet.md) covers `greet NAME`, names with spaces, and names that start with `-`.
- [Help text](./help.md) covers `--help` and `-h` for the program and for `greet`.
- [Usage errors](./usage-errors.md) covers a missing command, a missing name, an unknown command and extra arguments.
