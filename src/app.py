import argparse
import shutil
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import as_file, files
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Self


def prepare_site(destination: Path) -> None:
    with as_file(files("src")) as package:
        shutil.copytree(package / "web", destination, dirs_exist_ok=True)
        shutil.copytree(
            package,
            destination / "src",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".gitkeep", "web"),
        )
    vendor = destination / "vendor"
    vendor.mkdir()
    for name in ("brython.js", "brython_stdlib.js"):
        (vendor / name).write_bytes(files("brython").joinpath("data", name).read_bytes())


class EditorHandler(SimpleHTTPRequestHandler):
    def list_directory(self: Self, path: str) -> None:
        self.send_error(404, "Not found")
        return None

    def end_headers(self: Self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def port_number(value: str) -> int:
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("port must be an integer") from error
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 0 and 65535")
    return port


def main() -> None:
    parser = argparse.ArgumentParser(description="Risk of Rain 2 Save Editor")
    parser.add_argument("--port", type=port_number, default=8000, help="local port (default: 8000)")
    parser.add_argument("--open", action="store_true", help="open the editor in your browser")
    args = parser.parse_args()

    with TemporaryDirectory(prefix="ror2-editor-") as temporary:
        directory = Path(temporary)
        prepare_site(directory)
        handler = partial(EditorHandler, directory=str(directory))
        try:
            server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
        except OSError as error:
            parser.exit(1, f"Cannot start local server: {error}\nTry --port 8001.\n")
        with server:
            url = f"http://127.0.0.1:{server.server_port}/"
            print(f"Risk of Rain 2 Save Editor: {url}", flush=True)
            print("Press Ctrl+C to stop.", flush=True)
            if args.open:
                webbrowser.open(url)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")
