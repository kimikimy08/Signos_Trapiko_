from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def error_404(request, exception):
   context = {}
   return render(request,'404.html', context)

def error_500(request):
    context = {}
    return render(request,'500.html', context)