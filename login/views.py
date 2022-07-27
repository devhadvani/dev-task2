from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Custom,Topic,Blog
from django.contrib.auth import authenticate,login,logout
from .forms import CustomCreationForm,BlogForm, TopicForm
from django.db.models import Q

# Create your views here.
def home(request):
    q = request.GET.get('q') 
    if request.GET.get('q') != None:
        blog = Blog.objects.filter(
            Q( topic__name__icontains=q) &
            Q(draft = False) ) 
        
    else:
        blog = Blog.objects.filter(draft=False)


        
    topic = Topic.objects.all()
    drafts = Blog.objects.filter(draft=True)
    
    context = {'blog':blog,'topics':topic,'list':q,"draft":drafts}
    return render(request,'home.html',context)

def about(request):
        return render(request,'about.html')

def register(request):
    form = CustomCreationForm()
    if request.method == "POST":

        form = CustomCreationForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(commit  = False)
            user.username = user.username.lower()
            user.save()
            print(user)
            return redirect('log')
  
    return render(request,"register.html",{'form':form})


def log(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('Invalid Username or Password')
            return redirect('log')



    else:
        return render(request, 'login.html')
    return render(request,'login.html')

def logout_form(request):
    logout(request)
    return redirect('home')

def create_blog(request):
    form = BlogForm()
    form = BlogForm(request.POST,request.FILES)
    if form.is_valid():

            name = form.save(commit  = False)
            name.save()
            print(name)
            return redirect('create_blog')
    
    return render(request,'blogform.html',{'form':form})

def create_topic(request):
    form = TopicForm()
    if request.method == "POST":

        form = TopicForm(request.POST)
        if form.is_valid():

            name = form.save(commit  = False)
            name.save()
            print(name)
            return redirect('create_topic')

    
    return render(request,'topicform.html',{'form':form})

    
def blog(request,pk):
    blogs = Blog.objects.get(id=pk)
    
    context = { 'blogs':blogs}
    return render(request,'blog.html',context)