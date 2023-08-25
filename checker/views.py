from asgiref.sync import async_to_sync
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, CreateView

from checker.models import UploadedFile
from checker.tasks import check_file_errors

import websocket


# Create your views here.
class IndexView(TemplateView):
    template_name = 'checker/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['data'] = check_file_errors.delay(1)
        return context


class FilesView(LoginRequiredMixin, ListView):
    template_name = 'checker/files.html'

    def get_queryset(self):
        queryset = UploadedFile.objects.filter(user=self.request.user)
        return queryset


class DeleteFileView(View):
    def post(self, request, file_id):
        file = UploadedFile.objects.get(id=file_id)
        file.status = UploadedFile.DELETED
        file.save()
        return redirect('checker:files')


class UpdateFileView(View):
    def post(self):
        new_file = self.request.FILES('')
        UpdateFileView = self.kwargs['file_id']


class CreateNewFile(View):
    def post(self):
        form = UploadedFileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            uploaded_file = form.save()

            ws_url = 'ws://{}{}'.format(self.request.get_host(), reverse('consumer_url'))
            async_to_sync(websocket.connect)(ws_url)

            async_to_sync(websocket.send)('')
            return redirect('checker:files')

    def get(self):
        form = UploadedFileForm()
        return render(self.request, 'checker/files.html', {'form': form})
