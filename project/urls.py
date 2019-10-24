from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from matomo_monorail.views import proxy_js, proxy_php

from .views import ip


urlpatterns = [
    path('matomo.js', proxy_js),
    path('matomo.php', proxy_php),
    path('mailinglist/', include('mailinglist.urls')),
    path('admin/', admin.site.urls),
    path('ip/', ip),
    path('', TemplateView.as_view(template_name='index.html')),
]
