from django.shortcuts import render
from django.db import connection
import os, time
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
from django.http import JsonResponse, HttpResponse

def getchatts(request):
    if request.method != 'GET':
        return HttpResponse(status=404)

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM chatts ORDER BY time DESC;')
    rows = cursor.fetchall()

    response = {}
    response['chatts'] = rows
    return JsonResponse(response)

def getimages(request):
    if request.method != 'GET':
        return HttpResponse(status=404)

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM images ORDER BY time DESC;')
    rows = cursor.fetchall()

    response = {}
    response['chatts'] = rows
    return JsonResponse(response)


from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def postchatt(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    username = json_data['username']
    message = json_data['message']
    cursor = connection.cursor()
    cursor.execute('INSERT INTO chatts (username, message) VALUES '
                   '(%s, %s);', (username, message))
    return JsonResponse({})

@csrf_exempt
def postimages(request):
    if request.method != 'POST':
        return HttpResponse(status=400)

    # loading form-encoded data
    username = request.POST.get("username")
    message = request.POST.get("message")

    if request.FILES.get("image"):
        content = request.FILES['image']
        filename = username+str(time.time())+".jpeg"
        fs = FileSystemStorage()
        filename = fs.save(filename, content)
        imageurl = fs.url(filename)
    else:
        imageurl = None

    if request.FILES.get("video"):
        content = request.FILES['video']
        filename = username+str(time.time())+".mp4"
        fs = FileSystemStorage()
        filename = fs.save(filename, content)
        videourl = fs.url(filename)
    else:
        videourl = None

    cursor = connection.cursor()
    cursor.execute('INSERT INTO images (username, message, imageurl, videourl) VALUES '
                   '(%s, %s, %s, %s);', (username, message, imageurl, videourl))

    return JsonResponse({})
