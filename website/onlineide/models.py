from django.db import models
from django import forms
from datetime import datetime

#class User(models.Model):
   #email = models.CharField(required=True)
   #name = models.CharField(max_length=50)
   #password = models.Field(max_length=20)
   #apikey = models.CharField(max_length=20)
   
class Snippet(models.Model):
   creator = models.ForeignKey('auth.User', related_name='snippets')
   snippet = models.TextField()
   snippetdate = models.DateTimeField(default=datetime.now, blank=True)
   isPublic = models.BooleanField()
   isPermanent = models.BooleanField()
   language = models.CharField(max_length=10)
   
   def getId(self):
       return self.pk;

class Filestats(models.Model):
   creator = models.ForeignKey('auth.User', related_name='filestat')
   snippetid = models.ForeignKey(Snippet, related_name='coding')
   error = models.TextField()
   result = models.TextField()
   stats = models.TextField()

class IDEForm(forms.Form):
   name = forms.CharField()
   language = forms.CharField()
   snippet = forms.CharField(widget = forms.Textarea())
