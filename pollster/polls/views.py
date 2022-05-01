from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from django.template import loader
from django.urls import reverse

# Create your views here.

# get questions and display them
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific questions and choices
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question doesn't exist")
    return render(request, 'polls/details.html', { 'question' : question })

# Get question and display the results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', { 'question' : question })

# vote for a question choice
def vote(request, question_id):
    # print(request.POST['choice])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : 'You didnot select a choice.',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # always retuen an HttpResponseRedirect after successfully dealing with POST data. This prevents fata from being posted twice if a user hits the back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question, id,)))
