"""oser_cs URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from .views import ReactAppView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^api/docs/', include_docs_urls(title='OSER_CS API')),
    url('api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^$', ReactAppView.as_view()),
]

# DEVELOPMENT ONLY
# Directly serving static files in production is inefficient
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)