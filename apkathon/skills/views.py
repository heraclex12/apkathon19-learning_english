from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient

# Create your views here.
def writing(request):
    conn = MongoClient()
    db = conn.MyProject
    collection = db.Writing
    records = collection.find()
    topics = list(records)
    context = {'topic' : topics[0]}
    return render(request, 'writing.html', context)

def index(request):
    return render(request, 'index.html',{})