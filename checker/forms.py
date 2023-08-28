from django import forms
from django.contrib.auth import get_user_model

from checker.models import UploadedFile, validate_file_extension


class AddFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'd-none', 'type': 'file'}), required=False)

    class Meta:
        model = UploadedFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            validate_file_extension(file)
        return file


class RewriteFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'd-none', 'type': 'file'}), required=False)

    class Meta:
        model = UploadedFile
        fields = ['file']
