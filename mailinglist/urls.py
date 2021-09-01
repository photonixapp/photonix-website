from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('confirmation/', TemplateView.as_view(template_name='mailinglist/confirmation.html'), name='confirmation'),
    path('preferences/', views.preferences, name='preferences'),
    path('preferences/updated/', TemplateView.as_view(template_name='mailinglist/preferences_updated.html'), name='preferences-updated'),
]
