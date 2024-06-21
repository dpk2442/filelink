from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render, resolve_url
from django.views.decorators.http import require_GET
from django_sendfile import sendfile

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
    shares = models.Share.objects.filter(user=request.user)
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


@login_required
def delete_share(request: HttpRequest, share_id: int):
    share = get_object_or_404(models.Share, id=share_id, user=request.user)
    if request.method == "POST":
        share.delete()
        return redirect("shares:index")

    return render(request, "shares/share_delete.html", dict(
        title="Delete Share",
        share=share,
    ))


@require_GET
def download_share(request: HttpRequest, share_slug: str):
    share = get_object_or_404(models.Share, slug=share_slug)
    root_path: Path = settings.FL_FILES_PATH
    share_path = f"{share.directory}/{share.name}" \
        if share.directory else share.name
    return sendfile(request, (root_path / share_path).as_posix(), attachment=True, attachment_filename=share.name)
