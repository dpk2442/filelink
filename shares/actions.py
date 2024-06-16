import os
from pathlib import Path
from typing import Dict, Tuple

from django.conf import settings
from django.shortcuts import redirect

from shares.exceptions import InvalidRequestPathException


def get_directories_and_files(requested_path: Path) -> Tuple[Dict, Dict, Path]:
    files_root_path: Path = settings.FL_FILES_PATH
    scan_path = (files_root_path / requested_path).resolve()
    if requested_path.is_absolute() or not scan_path.is_relative_to(files_root_path):
        raise InvalidRequestPathException()

    directories = []
    files = []
    with os.scandir(scan_path) as scan:
        for f in scan:
            if f.is_dir():
                directories.append(dict(
                    name=f"{f.name}/",
                    path=(scan_path / f.name).relative_to(files_root_path),
                ))
            elif f.is_file():
                files.append(dict(
                    name=f.name,
                ))

    directories.sort(key=lambda x: x["name"])
    files.sort(key=lambda x: x["name"])

    parent_path = None
    if scan_path != files_root_path:
        parent_path = (scan_path / "..").resolve().relative_to(files_root_path)

    return (directories, files, parent_path)
