"""python3 -m trial greet NAME"""
import argparse
import sys

GREET_HELP = "Print a greeting for NAME"


def greeting(name: str) -> str:
    return f"Hello, {name}!"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="trial", description="A tiny program for testing the factory.")
    commands = parser.add_subparsers(dest="command", metavar="command", required=True)
    greet = commands.add_parser("greet", help=GREET_HELP, description=GREET_HELP)
    greet.add_argument("name", help="who to greet")
    greet.add_argument("--shout", action="store_true", help="print the greeting in capital letters")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "greet":
        text = greeting(args.name)
        print(text.upper() if args.shout else text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
