from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.

def index(request):
    return HttpResponse("<h1>Pollarize</h1>")
