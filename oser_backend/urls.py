"""General URL Configuration."""

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls
from rest_auth.views import PasswordResetConfirmView

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
    url(r'^api/rest-auth/', include('rest_auth.urls')),
    # API docs
    url(r'^api/docs/', include_docs_urls(title='OSER_CS API', public=False)),
    # Markdown 3rd party app
    url(r'^markdownx/', include('markdownx.urls')),
    re_path(r'^rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
