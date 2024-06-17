import os
from pathlib import Path

from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from shares import actions
from shares.exceptions import InvalidRequestPathException


def index(_: HttpRequest):
    return redirect("shares:files")


@require_GET
def files(request: HttpRequest):
    try:
        requested_path = Path(request.GET.get("path", default="."))
        (files, directories, parent_path) = actions.get_directories_and_files(
            requested_path)
    except InvalidRequestPathException:
        return redirect("shares:files")

    return render(request, "shares/files.html", dict(
        title="Browse Files",
        parent_path=parent_path,
        files=directories + files,
    ))
