from django import forms

from shares import models


class ShareForm(forms.ModelForm):
    class Meta:
        model = models.Share
        fields = ["directory", "name", "download_enabled", "force_download"]
