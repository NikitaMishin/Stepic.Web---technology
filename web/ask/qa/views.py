from django.shortcuts import render,redirect
from qa.models import *
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.paginator import Paginator, InvalidPage,EmptyPage
from qa.forms import *
def test (request):
    return HttpResponse('OK')
    
    

def displayPopularQuestion(request):

    page = request.GET.get('page',1)
    paginator= Paginator(Question.objects.popular(),10)
    paginator.baseurl ="/popular/?page="
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)    
    return render(request,"popular.html",{
        'questions':page.object_list,
        'paginator':paginator,
        'page':page,
    })    
    
def displayNewQuestion(request):
    page = request.GET.get('page',1)
    paginator= Paginator(Question.objects.new(),10)
    paginator.baseurl ="/?page="
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request,"new.html",{
        'questions':page.object_list,
        'paginator':paginator,
        'page':page,
    })    
           
def ask(request):
    if request.method=="POST":
        form = AskForm(request.POST)
        if form.is_valid():
            post = form.save()
            url =  post.get_url() 
            return HttpResponseRedirect(url)
    else:
        form = AskForm(user_id=request.user.id)
    return render(request,"ask.html",{"form":form})            

def undoQuestion(request,question_id):
    user_id=request.user.id
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404
    answers = Question.objects.getAnswers(question)
    if request.method=="POST":   
        form = AnswerForm(request.POST)
        if form.is_valid():
            #form.author=request.user
            #form.question=question
            post = form.save(request.user,question)
            url =post.get_url() 
            return HttpResponseRedirect(url) 
    else:
        form = AnswerForm(initial={'question': question.id})
    return render(request,"q.html",{"question":question,"answers":answers,"form":form})  
    





# Create your views here.
