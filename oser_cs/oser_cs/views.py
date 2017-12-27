from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os


class ReactAppView(View):

    def get(self, request):
        try:
            with open(os.path.join(settings.REACT_APP_DIR,
                                   'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                "File index.html not found. Build your React app !",
                status=501,
            )
