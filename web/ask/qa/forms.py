from django.db import models
from django.contrib.auth.models import User
from django import forms
from qa.models import *


class AskForm(forms.Form):
    title = forms.CharField(max_length=200)
    text =  forms.CharField(widget=forms.Textarea())
    def clean(self):
        pass      
    def __init__(self,*args,**kwargs):    
        try:
            self.author = User.objects.get(id = kwargs.pop("user_id",1))
        except User.DoesNotExist:
            self.author = User.objects.get(id = 1)
        super(AskForm,self).__init__(*args,**kwargs) 
   
    def save(self):
        question = Question(**self.cleaned_data)
        question.author = self.author
        question.save()
        return question



class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())
    question = forms.IntegerField(widget=forms.HiddenInput())

   # def _for()_init__(self,*args,**kwargs):
        
       
    #    super(AnswerForm,self).__init__(args,**kwargs)
    
    def clean(self):
        pass
                 
    def save(self,useros,question):
        self.cleaned_data['author'] = useros
        self.cleaned_data['question']=question
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer
        
   
