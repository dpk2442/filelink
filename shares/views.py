from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, redirect, render, resolve_url
from django.views.decorators.http import require_GET

from shares import actions, forms, models
from shares.exceptions import InvalidRequestPathException


def index(_: HttpRequest):
    return redirect("shares:shares")


@login_required
@require_GET
def files(request: HttpRequest):
    try:
        requested_path = Path(request.GET.get("path", default="."))
        (directories, files, parent_path) = actions.get_directories_and_files(
            requested_path)
    except InvalidRequestPathException:
        return redirect("shares:files")

    return render(request, "shares/files.html", dict(
        title="Browse Files",
        parent_path=parent_path,
        directories=directories,
        files=files,
    ))


@login_required
@require_GET
def shares(request: HttpRequest):
    shares = get_list_or_404(models.Share, user=request.user)
    return render(request, "shares/shares.html", dict(
        title="Shares",
        shares=shares,
    ))


@login_required
def new_share(request: HttpRequest):
    if request.method == "POST":
        form = forms.ShareForm(request.POST)
        if form.is_valid():
            share = form.save(commit=False)
            share.user = request.user
            share.save()
            return redirect("shares:index")
    else:
        directory = ""
        name = ""
        if request_path := request.GET.get("path"):
            path = Path(request_path)
            name = path.name
            if (parent := path.parent.as_posix()) != ".":
                directory = parent

        form = forms.ShareForm(dict(directory=directory, name=name))

    return render(request, "shares/share_form.html", dict(
        title="New Share",
        url=resolve_url("shares:new_share"),
        form=form,
    ))
