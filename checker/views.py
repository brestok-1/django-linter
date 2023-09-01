import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView

from checker.forms import AddFileForm, RewriteFileForm
from checker.models import UploadedFile


# Create your views here.
class IndexView(TemplateView):
    template_name = 'checker/index.html'


class FilesView(LoginRequiredMixin, CreateView):
    template_name = 'checker/files.html'
    success_url = reverse_lazy('checker:files')
    form_class = AddFileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = UploadedFile.objects.filter(user=self.request.user).order_by('time_created')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteFileView(View):
    def post(self, request, file_id):
        file = UploadedFile.objects.get(id=file_id)
        file.status = UploadedFile.DELETED
        os.remove(file.file.path)
        file.save(task_need=False)
        return redirect('checker:files')


class UpdateFileView(UpdateView):
    pk_url_kwarg = 'pk'
    model = UploadedFile
    form_class = RewriteFileForm
    template_name = 'checker/update_file.html'
    success_url = reverse_lazy('checker:files')

    def form_valid(self, form):
        form.instance.status = UploadedFile.OVERWRITTEN
        form.instance.check_result = ''
        return super().form_valid(form)


class GetCheckResult(DetailView):
    template_name = 'checker/file_report.html'
    pk_url_kwarg = 'pk'
    model = UploadedFile

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status == UploadedFile.DELETED:
            raise Http404('Страница не найдена или удалена')
        return super().get(request, *args, **kwargs)
