from django.shortcuts import render

# Create your views here.

def complete_view(request):
    return render(request, 'registration/complete.html')