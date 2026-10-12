# factory-trial

A tiny command-line program used to test the FirstMate factory end to end. It has no dependencies beyond Python 3.

## Use

```bash
python3 -m trial greet Ada
```

You will receive a greeting for the name you give: `Hello, Ada!`. `python3 -m trial greet --help` describes the
command.

## Tests

```bash
python3 -m unittest discover -t . -s tests
```

The same command runs in CI on every pull request and on every push to `main`.
