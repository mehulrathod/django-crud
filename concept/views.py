from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404

from concept.models import signup


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        s = signup.objects.filter(email=email).count()
        if s > 0:
            return HttpResponse("/login/")
        else:
            post = signup()
            post.email = request.POST.get("email")
            post.username = request.POST.get("username")
            post.password = request.POST.get("password")
            post.date = datetime.now().date()
            post.time = datetime.now().time()
            post.save()
            return HttpResponseRedirect('/login/')
    else:
        return render(request, "register.html")


def static_sign(request):
    s = signup.objects.filter(email="akhil46@gmail.com").count()
    if s > 0:
        return HttpResponse("Already registered!")
    else:
        post = signup()
        post.email = "akhil46@gmail.com"
        post.username = "Akhil Rathod"
        post.password = "rammohansigngh"
        post.date = datetime.now().date()
        post.time = datetime.now().time()
        post.save()
        return HttpResponse('successfully  rtegistered')


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        s = signup.objects.filter(email=email, password=password).count()
        if s > 0:
            sel = get_object_or_404(signup, email=email, password=password)
            request.session["userid"] = sel.id
            request.session["email"] = sel.email
            request.session["password"] = sel.password
            request.session["username"] = sel.username
            return HttpResponseRedirect('/')
        else:
            return render(request, "login.html", {"msg": "wrong email or password"})
    else:
        return render(request, "login.html")


def dashboard(request):
    s = signup.objects.all().order_by("-id")
    return render(request, "dashboard.html", {"data": s})


def edit_profile(request):
    userid = request.session['userid']
    if request.method == "POST":
        post = get_object_or_404(signup, id=userid)
        post.username = request.POST.get("username")
        post.email = request.POST.get("email")
        post.password = request.POST.get("password")
        post.date = datetime.now().date()
        post.time = datetime.now().time()
        post.save()
        return HttpResponseRedirect("/login/")
    else:
        sel = signup.objects.filter(id=userid)
        return render(request, "edit_profile.html", {"data": sel})


def change_password(request):
    if request.method == "POST":
        userid = request.session['userid']
        sel = get_object_or_404(signup, id=userid)
        db_pwd = sel.password
        new_pwd = request.POST.get("new_pwd")
        current_pwd = request.POST.get("current_pwd")
        if new_pwd == current_pwd:
            sel.password = current_pwd
            sel.save()
            return HttpResponseRedirect('/login/')
        else:
            return HttpResponse("your old_pwd and new_pwd didn't matched")
    else:
        return render(request, "change_password.html")


def profile(request):
    userid = request.session['userid']
    if request.method == "POST":
        sel = get_object_or_404(signup, id=userid)
        myfile = request.FILES['images']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        sel.images = uploaded_file_url
        request.session["profile"] = uploaded_file_url
        sel.save()
        s1 = signup.objects.filter(id=userid)
        return render(request, "profile.html", {"data": s1})
    else:
        s1 = signup.objects.filter(id=userid)
        return render(request, "profile.html", {"data": s1})