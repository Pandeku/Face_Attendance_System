from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect


# Create your views here.
def page_not_found(request):
    return render(request, 'error_html/404.html')


def page_error(request):
    return render(request, 'error_html/500.html')


def permission_denied(request):
    return render(request, 'error_html/403.html')


def bad_request(request):
    return render(request, 'error_html/400.html')


def index(request):
    return render(request, '_index/index.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


