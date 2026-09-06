#!/usr/bin/env python3
"""Serve a presentation folder on loopback only; no directory listings or symlinks."""
import argparse
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


class PreviewHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(HTTPStatus.FORBIDDEN, "Directory listing disabled; open the HTML filename")
        return None

    def allowed_path(self):
        base = Path(self.directory).resolve()
        request = unquote(urlsplit(self.path).path)
        # Browser URLs use forward slashes; reject Windows separators and NUL.
        if "\\" in request or "\x00" in request:
            return False
        parts = [part for part in request.split("/") if part]
        if any(part in (".", "..") or ":" in part for part in parts):
            return False
        target = base.joinpath(*parts)
        current = base
        for part in parts:
            current = current / part
            if current.is_symlink():
                return False
        if target.is_dir() and any((target / name).is_symlink() for name in ("index.html", "index.htm")):
            return False
        try:
            target.resolve().relative_to(base)
        except (ValueError, OSError):
            return False
        return True

    def send_head(self):
        if not self.allowed_path():
            self.send_error(HTTPStatus.FORBIDDEN, "Path outside preview folder or symbolic link")
            return None
        return super().send_head()

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def make_server(directory, port):
    directory = Path(directory).resolve(strict=True)
    if not directory.is_dir():
        raise ValueError("Preview directory must be a folder")
    return ThreadingHTTPServer(("127.0.0.1", port), partial(PreviewHandler, directory=str(directory)))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default=".", type=Path)
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("port must be between 0 and 65535")
    try:
        with make_server(args.directory, args.port) as server:
            print("Local preview: http://127.0.0.1:" + str(server.server_port) + "/<your-file>.html", flush=True)
            print("Press Ctrl+C to stop. No files are uploaded.", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except (OSError, ValueError) as exc:
        print("Preview failed: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
