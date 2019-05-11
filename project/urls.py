from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('mailinglist/', include('mailinglist.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='mailinglist/confirmation.html'))
]
