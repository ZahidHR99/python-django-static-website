from django.shortcuts import render

# home page
def home(request):
    return render(request, 'home.html')

# about page
def about(request):
    return render(request, 'about.html')

# projects page  
def projects(request):
    return render(request, 'projects.html')

# testimonial page
def testimonial(request):
    return render(request, 'testimonial.html')

# hire page
def hire(request):
    return render(request, 'hire.html')

# blog page
def contact(request):
    return render(request, 'contact.html')