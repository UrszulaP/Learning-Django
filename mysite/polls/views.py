from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'  # default: <app name>/<model name>_<view type>.html -> polls/question_list.html
    context_object_name = 'latest_question_list'  # context variable name, default: question_list (question for DetailView)

    def get_queryset(self):  # overrides default method
        """Return the last five published questions
        Method overriding default context - list of all model objects (should then be set: model = Question)"""
        return Question.objects.filter(
            pub_date__lte=timezone.now()  # lte means less than or equal to
        ).order_by('-pub_date')[:5]  # "-" means reverse order, returns a list


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data.
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn`t select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents data from being posted twice if a user hits the Back button.
        # reverse() helps avoid having to hardcode a URL in the view function
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
