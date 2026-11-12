from __future__ import annotations

__all__: list[str] = ["main", "parse_args", "run"]

import argparse
import io
import logging
import tomllib
from collections.abc import Iterable
from importlib import metadata
from typing import Any


def get_from_file(
    *,
    infile: str,
    keys: Iterable[str],
) -> Any:
    data: dict[str, Any]
    stream: io.BufferedReader
    x: str
    y: int | str
    if infile == "-":
        data = tomllib.loads(input())
    else:
        with open(infile, "rb") as stream:
            data = tomllib.load(stream)
    for x in keys:
        try:
            y = str(x) if isinstance(data, dict) else int(x)
            data = data[y]
        except Exception:
            return None
    return data


def main(args: Iterable[str] | None = None) -> int:
    space: argparse.Namespace
    try:
        space = parse_args(args)
        run(**vars(space))
    except SystemExit as exit:
        if isinstance(exit.code, int):
            return int(exit.code)
        else:
            return int(bool(exit.code))
    except BaseException as exc:
        logging.exception(exc)
        return 1
    else:
        return 0


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser: argparse.ArgumentParser
    version: str
    parser = argparse.ArgumentParser(
        add_help=False,
        fromfile_prefix_chars="@",
        prog="toml_get",
    )
    parser.add_argument(
        "--default",
    )
    parser.add_argument(
        "--infile",
        action="append",
        default=[],
        dest="infiles",
    )
    parser.add_argument(
        "--key",
        action="append",
        default=[],
        dest="keys",
    )
    parser.add_argument(
        "--outfile",
        default="-",
    )
    parser.add_argument(
        "--outstring",
        default="%s\n",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
    )
    version = "%(prog)s, version " + metadata.version("toml_get")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        help="show the version and abort",
        version=version,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="show this message and abort",
    )
    return parser.parse_args(args)


def run(
    *,
    default: object = None,
    infiles: Iterable[str] = (),
    keys: Iterable[str] = (),
    outfile: str = "-",
    outstring: str = "%s\n",
    overwrite: bool = False,
) -> None:
    ans: object
    infile: str
    stream: Any
    ans = None
    for infile in infiles:
        ans = get_from_file(
            infile=infile,
            keys=keys,
        )
        if ans is not None:
            break
    if ans is not None:
        try:
            ans = outstring % ans
        except Exception:
            ans = None
    if ans is None:
        ans = default
    if ans is None:
        return
    if outfile == "-":
        print(ans, end="")
        return
    with open(outfile, "w" if overwrite else "wb") as stream:
        print(ans, end="", file=stream)
