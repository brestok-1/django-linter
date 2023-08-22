from django.shortcuts import render
from django.views.generic import TemplateView
from checker.tasks import check_file_errors


# Create your views here.
class IndexView(TemplateView):
    template_name = 'checker/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = check_file_errors.delay(1)
        return context

