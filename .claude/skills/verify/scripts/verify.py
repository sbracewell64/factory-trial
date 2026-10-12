#!/usr/bin/env python3
"""Drive the trial CLI the way a user does and keep a transcript of every run.

  verify.py launch --evidence DIR        create a run directory, print RUN=<path>
  verify.py doctor --run RUN             read-only: is this checkout worth driving?
  verify.py drive  --run RUN LABEL [--exit N] [--stdout TEXT] [--stderr-has TEXT] -- ARGS...
                                         run `python3 -m trial ARGS...` from the repo root
  verify.py cleanup --run RUN            remove the run directory, keep the evidence
"""
import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
TIMEOUT = 30


def git_head():
    r = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def python_version(python):
    r = subprocess.run([python, "--version"], capture_output=True, text=True)
    return (r.stdout or r.stderr).strip()


def load(run):
    with open(os.path.join(run, "run.json")) as f:
        return json.load(f)


def launch(a):
    python = shutil.which("python3")
    if not python:
        sys.exit("launch: python3 is not on PATH")
    evidence = os.path.abspath(a.evidence)
    os.makedirs(evidence, exist_ok=True)
    run = tempfile.mkdtemp(prefix="trial-verify.")
    if os.path.commonpath([run, evidence]) == run:
        sys.exit("launch: the evidence directory must not be inside the run directory")
    state = {"repo": REPO, "python": python, "python_version": python_version(python),
             "head": git_head(), "evidence": evidence}
    with open(os.path.join(run, "run.json"), "w") as f:
        json.dump(state, f, indent=2)
    print(f"RUN={run}")
    print(f"repo={REPO} head={state['head']} {state['python_version']} evidence={evidence}")


def doctor(a):
    s = load(a.run)
    checks = [
        ("repo is trial", os.path.isfile(os.path.join(s["repo"], "trial", "__main__.py"))),
        ("python3 unchanged", python_version(s["python"]) == s["python_version"]),
        ("head unchanged", git_head() == s["head"]),
        ("evidence writable", os.access(s["evidence"], os.W_OK)),
    ]
    r = subprocess.run([s["python"], "-m", "trial", "--help"], cwd=s["repo"], capture_output=True,
                       text=True, timeout=TIMEOUT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    checks.append(("trial --help answers", r.returncode == 0 and r.stdout.startswith("usage: trial")))
    for name, ok in checks:
        print(f"{'ok  ' if ok else 'FAIL'} {name}")
    sys.exit(0 if all(ok for _, ok in checks) else 1)


def drive(a, child):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,60}", a.label):
        sys.exit(f"drive: label {a.label!r} must be a plain file name")
    s = load(a.run)
    cmd = [s["python"], "-m", "trial", *child]
    r = subprocess.run(cmd, cwd=s["repo"], capture_output=True, text=True, timeout=TIMEOUT,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    failed = []
    if a.exit is not None and r.returncode != a.exit:
        failed.append(f"exit {r.returncode} != {a.exit}")
    if a.stdout is not None and r.stdout != a.stdout.replace("\\n", "\n"):
        failed.append(f"stdout {r.stdout!r} != {a.stdout!r}")
    if a.stderr_has is not None and a.stderr_has not in r.stderr:
        failed.append(f"stderr lacks {a.stderr_has!r}")
    verdict = "PASS" if not failed else "FAIL: " + "; ".join(failed)
    transcript = (f"$ cd {s['repo']} && python3 -m trial {shlex.join(child)}\n"
                  f"head: {s['head']}\n{s['python_version']}\nexit: {r.returncode}\n"
                  f"--- stdout ---\n{r.stdout}--- stderr ---\n{r.stderr}--- verdict ---\n{verdict}\n")
    path = os.path.join(s["evidence"], f"{a.label}.txt")
    with open(path, "w") as f:
        f.write(transcript)
    print(transcript + f"transcript: {path}")
    sys.exit(0 if not failed else 1)


def cleanup(a):
    s = load(a.run)
    shutil.rmtree(a.run)
    kept = sorted(os.listdir(s["evidence"]))
    print(f"removed {a.run}; evidence kept in {s['evidence']}: {', '.join(kept) or '(none)'}")


def main():
    argv = sys.argv[1:]
    child = []
    if "--" in argv:
        i = argv.index("--")
        argv, child = argv[:i], argv[i + 1:]
    p = argparse.ArgumentParser(prog="verify.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("launch").add_argument("--evidence", required=True)
    for name in ("doctor", "cleanup"):
        sub.add_parser(name).add_argument("--run", required=True)
    d = sub.add_parser("drive")
    d.add_argument("--run", required=True)
    d.add_argument("label")
    d.add_argument("--exit", type=int)
    d.add_argument("--stdout")
    d.add_argument("--stderr-has")
    a = p.parse_args(argv)
    if a.cmd == "drive":
        drive(a, child)
    elif child:
        p.error("only drive takes arguments after --")
    else:
        {"launch": launch, "doctor": doctor, "cleanup": cleanup}[a.cmd](a)


if __name__ == "__main__":
    main()
