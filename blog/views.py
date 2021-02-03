from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def newpost(request):
    return render(request, 'blog/newpost.html')
