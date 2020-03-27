from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from matomo_monorail.views import proxy_js, proxy_php

from blog.sitemaps import BlogSitemap
from .sitemaps import StaticViewSitemap
from .views import ip


sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('matomo.js', proxy_js),
    path('matomo.php', proxy_php),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('ip/', ip),
    path('mailinglist/', include('mailinglist.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
