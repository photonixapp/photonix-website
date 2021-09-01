from django.conf.urls import url

from mailer import views

urlpatterns = [
    url(r'^mass-send/preview/', views.mass_send_preview),
    url(r'^mass-send/progress/', views.mass_send_progress),
    url(r'^mass-send/', views.mass_send),
    url(r'^r/(?P<tracker_id>\d+)/(?P<recipient_id>\d+)/(?P<salt>[A-Za-z0-9_-]+)/(?P<signature>[A-Za-z0-9_-]+)/$', views.tracking_redirect),
]
