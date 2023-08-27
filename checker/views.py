from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, CreateView, FormView

from checker.forms import AddFileForm, RewriteFileForm
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


class FilesView(LoginRequiredMixin, FormView):
    template_name = 'checker/files.html'
    success_url = reverse_lazy('checker:files')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = UploadedFile.objects.filter(user=self.request.user).order_by('time_created')
        return context

    def form_valid(self, form):
        file_id = form.save().id
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "file_group",
            {
                "type": "websocket.receive",
                "file_id": file_id,
            }
        )
        return super().form_valid(form)

    def get_form_class(self):
        return AddFileForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DeleteFileView(View):
    def post(self, request, file_id):
        file = UploadedFile.objects.get(id=file_id)
        file.status = UploadedFile.DELETED
        file.save()
        return redirect('checker:files')


class UpdateFileView(UpdateView):
    pk_url_kwarg = 'pk'
    model = UploadedFile
    form_class = RewriteFileForm
    # form = RewriteFileForm
    # fields = ['file']
    template_name = 'checker/update_file.html'
    success_url = reverse_lazy('checker:files')

    def form_valid(self, form):
        old_file = self.get_object().file
        old_file.delete(save=False)
        return super().form_valid(form)
