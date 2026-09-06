#!/usr/bin/env python3
"""Resolve a Python 3 interpreter and run a local helper without shell evaluation."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def probe(command):
    try:
        result = subprocess.run([*command, "-c", "import sys,json; print(json.dumps({'executable':sys.executable,'major':sys.version_info.major}))"], check=True, capture_output=True, text=True, timeout=10)
        info = json.loads(result.stdout)
        if info.get("major") != 3 or not Path(info.get("executable", "")).is_file():
            raise ValueError("Interpreter must be Python 3 with a real executable")
        return info["executable"]
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise ValueError("Cannot use Python interpreter: " + " ".join(command)) from exc


def resolve_python(explicit=None, environ=None, platform=None):
    environ = os.environ if environ is None else environ
    override = explicit or environ.get("CORPORATE_SLIDES_PYTHON")
    if override:
        # A configured interpreter is authoritative: do not quietly fall back.
        return probe([override])
    platform = sys.platform if platform is None else platform
    candidates = [["py", "-3"]] if platform == "win32" else []
    candidates += [[sys.executable], ["python3"], ["python"]]
    failures = []
    for command in candidates:
        if Path(command[0]).is_file() or shutil.which(command[0]):
            try:
                return probe(command)
            except ValueError as exc:
                failures.append(str(exc))
    raise ValueError("No usable Python 3 found. Set CORPORATE_SLIDES_PYTHON to its executable path. " + "; ".join(failures))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", help="Exact interpreter executable; invalid overrides fail")
    parser.add_argument("--print", action="store_true", dest="print_only")
    parser.add_argument("script", nargs="?", help="Helper filename under scripts/ or an explicit local path")
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        executable = resolve_python(args.python)
        if args.print_only:
            print(executable)
            return 0
        if not args.script:
            parser.error("provide a helper script, or --print")
        script = Path(args.script)
        if not script.is_absolute() and (ROOT / script).is_file():
            script = ROOT / script
        script = script.resolve(strict=True)
        if script.suffix.lower() != ".py":
            raise ValueError("Helper script must be a .py file")
        return subprocess.run([executable, str(script), *args.arguments], check=False).returncode
    except (OSError, ValueError) as exc:
        print("Python launch failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
