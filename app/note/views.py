from django.shortcuts import render

def notes(request):
    return render(request, 'notes/notes.html')
