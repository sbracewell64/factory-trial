---
name: verify
description: Drive the trial command-line program (python3 -m trial) the way a user does and capture a transcript per run. Use to prove a change to trial's greet command, its help text or its usage errors in the real program, not only in unit tests.
---

# Verify trial

trial is a short-lived Python 3 CLI with no dependencies and no server. A user runs `python3 -m trial greet NAME` from the repository root. The harness is `scripts/verify.py`: it runs the real module in a child process from the repository root, checks exit code and output, and writes one transcript per drive. Feature recipes are in `features/README.md`.

All commands below run from the repository root. Run each step as its own command.

## Launch

There is nothing to keep running. Launch records the run: the repository, its HEAD, the `python3` on `PATH` and its version, and the evidence directory.

```bash
python3 .claude/skills/verify/scripts/verify.py launch --evidence <evidence-dir>
```

Ready means it prints `RUN=/tmp/trial-verify.XXXXXXXX`. Pass that path as `--run` to every later step. Pick an evidence directory outside the run directory (launch refuses one inside it); a fresh directory per run keeps proofs apart.

## Doctor

Read-only. Run it after Launch and whenever a drive surprises you.

```bash
python3 .claude/skills/verify/scripts/verify.py doctor --run <RUN>
```

It prints one `ok`/`FAIL` line per check and exits 0 only when all pass: the checkout holds `trial/__main__.py`, `python3` and HEAD are the ones Launch recorded, the evidence directory is writable, and `python3 -m trial --help` exits 0 with `usage: trial`. A `head unchanged` failure means the checkout moved under you: launch again.

## Drive

```bash
python3 .claude/skills/verify/scripts/verify.py drive --run <RUN> <label> [--exit N] [--stdout TEXT] [--stderr-has TEXT] -- <trial args...>
```

- Everything after the first `--` goes to `python3 -m trial` unchanged, so a later `--` reaches trial itself (`-- greet -- --dash`).
- `--stdout` is the exact expected stdout; write a newline as `\n`. `--stderr-has` is a substring check. `--exit` is the expected exit code.
- The child runs with `PYTHONDONTWRITEBYTECODE=1` and a 30-second timeout, so a drive leaves no `__pycache__` and no process behind.
- Exit 0 means every given assertion held; exit 1 means one failed. The transcript says which.

Example: `... drive --run <RUN> greet-ada --exit 0 --stdout 'Hello, Ada!\n' -- greet Ada`. The recipes per feature are in `features/`.

## Evidence

Each drive writes `<evidence-dir>/<label>.txt`: the command and working directory, HEAD, Python version, exit code, stdout, stderr and the verdict. That transcript is the proof: it holds the user action and the resulting state.

- Drive the real entry point (`python3 -m trial ...`), never `trial.__main__.main()` or `greeting()` directly; the unit tests already do that.
- Assert both streams: a usage error must leave stdout empty and put `usage:` on stderr.
- trial writes no files. After a drive, `git status --short` should show no new paths from the drive; save its output next to the transcripts when a change could add side effects.

## Cleanup

```bash
python3 .claude/skills/verify/scripts/verify.py cleanup --run <RUN>
```

It removes only the run directory Launch created and lists the evidence it kept. No drive outlives its own command, so there is no process to stop; never kill by process name. Afterwards, list the evidence directory to confirm the transcripts survived.
