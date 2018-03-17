"""General URL Configuration."""

from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # Admin site
    url(r'^admin/', admin.site.urls),
    # Redirect the root to the admin site
    url(r'^$', RedirectView.as_view(url='admin/', permanent=True),
        name='index'),
    # API app
    url(r'^api/', include('api.urls')),
    # DRF authentication routes
    url(r'^api/auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    # API docs
    url(r'^api/docs/', include_docs_urls(title='OSER_CS API', public=False)),
    # Markdown 3rd party app
    url(r'^markdownx/', include('markdownx.urls')),
]
