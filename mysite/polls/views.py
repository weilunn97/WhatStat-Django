from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages

from .models import Choice, Question

'''
1. All views need to have a (HTTP) REQUEST associated with it
2. Views are the SERVER-SIDE LOGIC to handle HTTP Requests coming into our web server
(in this case, our local host) and serve appropriate HTTP Responses
3. Each render(...) method will take in 3 arguments and RETURNS a HttpResponse 
- request : HTTP request sent by a user (through a click event), or a webpage
(to generate pictures, text etc)    
- template_name : file name of the HTML file for Django to SERVE TO USER
- context : data that is passed to the template HTML file. You can map a variable
name to the value you wish to return via a dictionary {'var_name' : Question.objects.all()}
4. 
'''

def index(request):
    latestQuestionsList = Question.objects.order_by('-pub_date')[:5]
    contextDict = {'latestQuestionsList': latestQuestionsList}
    return render(request, 'polls/index.html', contextDict)


def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    contextDict = {'question': question}
    return render(request, 'polls/details.html', contextDict)


def results(request, question_id):
    return HttpResponse("You're looking at the results of Question %s" % question_id)


def votes(request, question_id):
    # Get the selected question object, else return a 404 not found error
    question = get_object_or_404(Question, pk=question_id)

    try:
        # Get the user choice (ie. selected radio button)
        # The POST request "key"/"name" refers to the name="..." in details.html
        # under the input type = ... section
        userChoice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        # Raise an error if unsuccessful
        return render(request=request,
                      template_name='polls/detail.html',
                      context={'question': question, 'error_message': 'You didn\'t select a choice'})

    return HttpResponse("Votes for Question %s" % question_id)
