from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.template import loader
from .models import Question, Choice
# Create your views here.

# INDEX THE LONG WAY
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list':latest_question_list,
#     }
#     return HttpResponse(template.render(context,request))

# INDEX THE SHORT WAY (function view)
#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#
# def detail(request, pk):
#     # GET OBJECT OR RAISE 404 LONG WAY
#     # try:
#     #     question = Question.objects.get(pk=pk)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#
#     # GET OBJECT OR RAISE 404 SHORT WAY (function view)
#
#     question = get_object_or_404(Question, pk=pk)
#     return render(request, 'polls/detail.html',{'question':question})

# RESULTS FUNCTION VIEW
# def results(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     return render(request, 'polls/results.html',{'question':question})

# CLASS BASED VIEWS

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last 5 published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

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

    def get_queryset(self):
        """
        Excludes results from any questions that aren't
        published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.pk,)))
