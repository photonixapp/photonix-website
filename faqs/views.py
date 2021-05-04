
from django.views.generic import DetailView, ListView
from faqs.models import Question


class QuestionList(ListView):
    """Question list view."""

    model = Question
    template_name = 'faqs/question_list.html'
    context_object_name = 'question_list'
    paginate_by = 10
    queryset = Question.objects.all().order_by('-created_at')


class QuestionDetail(DetailView):
    """Question detail view."""

    model = Question
    template_name = 'faqs/question_detail.html'
    context_object_name = 'question_obj'
