# Create your views here.
from django.http import HttpResponse
from onlineide.models import IDEForm, Snippet, Filestats
from django.contrib.auth.models import User
from django.template import RequestContext, Context
from django.shortcuts import render_to_response
from django.core.files import File
from sandbox import *
from onlineide.serializers import SnippetSerializer, UserSerializer, FilestatsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from onlineide.permissions import IsOwnerOrReadOnly

def index(request):
   language = request.POST.get('lang', '')
   name = request.POST.get('name', '')
   code_snippet = request.POST.get('snippet','')
   file_path = '/var/chroot/tmp/snippet.' + 'php'
   file_path = file_path.strip()
   if code_snippet:
       snippetObj = Snippet(snippet=code_snippet, language="php")
       snippetObj.save()
       print snippetObj.getId()
       f = open('/var/chroot/tmp/snippet' + str(snippetObj.getId()) + '.php', 'w')
       snippet_file = File(f)
       snippet_file.write(code_snippet)
       f.flush()
       snippet_file.closed
       #command = Command("chroot '/var/chroot' su - sandboxuser -c 'php /tmp/snippet.php')
       command = Command("schroot -c 'lucid' -d '/' -u sandboxuser -- php /tmp/snippet" + str(snippetObj.getId()) + ".php")
       output = command.run(timeout=5)
       print output
       #fout = open('/var/chroot/fout.txt', 'w')
       #out_file = File(fout)
       #out_file.write(output[2])
       #fout.flush()
       #ferr = open('/var/chroot/ferr.txt', 'w')
       #err_file = File(ferr)
       #err_file.write(output[1])
       #ferr.flush()   
       filestats = Filestats(snippetid=snippetObj,error=output[1],result=output[2])
       filestats.save()
   else:
       return render_to_response('index.html', {'form' : IDEForm }, RequestContext(request))
   return render_to_response('index.html', {'form' : IDEForm }, RequestContext(request))

class SnippetCreate(generics.CreateAPIView):
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def pre_save(self, obj):
        obj.creator = self.request.user
  
    def post_save(self, obj, created=False):
       f = open('/var/chroot/tmp/snippet' + str(obj.id) + '.php', 'w')
       snippet_file = File(f)
       snippet_file.write(obj.snippet)
       f.flush()
       snippet_file.closed
       command = Command("schroot -c 'lucid' -d '/' -u sandboxuser -- php /tmp/snippet" + str(obj.id) + ".php")
       output = command.run(timeout=3)
       filestats = Filestats(snippetid=obj, creator = self.request.user, error=output[1],result=output[2])
       filestats.save()

class SnippetDetail(generics.RetrieveAPIView):
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def pre_save(self, obj):
        obj.creator = self.request.user

class FilestatsDetail(APIView):

    def get(self, request, pk, format=None):
        filestat = Filestats.objects.filter(snippetid=pk, creator = self.request.user)
        if filestat:
            serializer = FilestatsSerializer(filestat[0])
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
