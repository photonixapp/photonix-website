from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from matomo_monorail.views import proxy_js, proxy_php

from faqs.sitemaps import QuestionSitemap
from blog.sitemaps import BlogSitemap
from .sitemaps import StaticViewSitemap
from .views import ip, landing


sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'faqs': QuestionSitemap
}

urlpatterns = [
    path('matomo.js', proxy_js),
    path('matomo.php', csrf_exempt(proxy_php)),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('faqs/', include('faqs.urls')),
    path('ip/', ip),
    path('landing/<slug:slug>/', landing),
    path('mailinglist/', include('mailinglist.urls')),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy-policy'),
    path('support/', TemplateView.as_view(template_name='support.html'), name='support'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
