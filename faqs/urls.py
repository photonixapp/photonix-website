
from django.urls import path
from faqs.views import QuestionList, QuestionDetail


urlpatterns = [
    path('', QuestionList.as_view(), name='faqs-list'),
    path('<slug:slug>/', QuestionDetail.as_view(), name='faqs-detail'),
]
