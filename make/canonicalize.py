__all__: list[str] = ["main", "parse_args", "run"]
import argparse
import logging
import sys
import tomllib
from collections import abc
from pathlib import Path

import tomli_w
from packaging.utils import canonicalize_name


def main(args: abc.Iterable[str] | None = None) -> int:
    space: argparse.Namespace
    try:
        space = parse_args(args)
        run(space.project)
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


def parse_args(args: abc.Iterable[str] | None = None) -> argparse.Namespace:
    parser: argparse.ArgumentParser
    parser = argparse.ArgumentParser(
        description="Canonicalize project.",
        fromfile_prefix_chars="@",
    )
    parser.add_argument("project", type=Path)
    return parser.parse_args(args)


def run(project: Path, /) -> None:
    name: str
    pyproject = project / "pyproject.toml"
    with open(pyproject, "rb") as instream:
        data = tomllib.load(instream)
    name = canonicalize_name(data["project"]["name"])
    data["project"]["name"] = name
    data["project"]["urls"][
        "Download"
    ] = f"https://pypi.org/project/{name}/#files"
    data["project"]["urls"]["Index"] = f"https://pypi.org/project/{name}/"
    data["project"]["urls"][
        "Source"
    ] = f"https://github.com/johannes-programming/{name}/"
    data["project"]["urls"][
        "Website"
    ] = f"https://{name}.johannes-programming.online/"
    with open(pyproject, "wb") as outstream:
        data = tomli_w.dump(data, outstream)


if __name__ == "__main__":
    sys.exit(main())
