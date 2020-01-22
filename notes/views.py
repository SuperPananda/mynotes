from django.shortcuts import render, redirect
from .models import Post, Category
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.contrib import auth
from .forms import PostForm

# Create your views here.

#Выводим список заметок
def post_list(request):
    posts = Post.objects.all().filter(author=request.user)
    posts = posts.order_by('-date')
    category = Category.objects.all()

    return render(request, 'notes/posts.html', context={'posts': posts, 'category': category, 'username': auth.get_user(request).username})

#Создание заметки
class PostCreate(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'notes/post_create_form.html', context={'form': form})

    def post(self,request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            bound_form.save_m2m()
            return redirect(new_post)
        return render(request, 'notes/post_create_form.html', context={'form': bound_form})

#Редактирование заметки
class PostUpdate(View):
    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(instance=post)
        return render(request, 'notes/post_update_form.html', context={'form': bound_form, 'post': post})

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(request.POST, instance=post)
        if bound_form.is_valid():
            new_post = bound_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            bound_form.save_m2m()
            return redirect(new_post)
        return render(request, 'notes/post_update_form.html', context={'form': bound_form, 'post': post})

#Зайти на страницу заметки
class PostDetail(View):
    def get(self, request, slug):
        post = Post.objects.filter(slug__iexact = slug).first()
        return render(request, 'notes/post_detail.html', context={'post': post})

#Добавить заметку в избранное
def favorites(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        post = Post.objects.filter(slug__iexact = post_id).first()
        post.favorite = True
        m = post
        m.save()
        return HttpResponse('success')
    else:
        return HttpResponse("unsuccesful")

#Удалить заметку из избранного
def unfavorites(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        post = Post.objects.filter(slug__iexact = post_id).first()
        post.favorite = False
        m = post
        m.save()
        return HttpResponse('success')
    else:
        return HttpResponse("unsuccesful")

#Формирование словаря для отправки в AJAX
def forming_dictionary(posts):
    response_data = {}
    out = []
    for elem in posts:
        out.append(elem.slug)

    response_data = dict.fromkeys(out)

    inp = []
    for elem in posts:
        inp.append(
        {"title": elem.title, "body": elem.body, "date": elem.date.strftime("%b. %d, %Y, %I:%M %p"), "category": elem.category.all().first().title, "favorite": elem.favorite, "slug": elem.slug , "url": elem.get_absolute_url(), "url_update":  elem.get_update_url()})

    l=0
    for key in response_data:
        response_data[key] = inp[l]
        l=l+1
    return response_data

#Сортировка заметок - AJAX
def sorting_notes(request):
    if request.POST.get('action') == 'post':
        option = request.POST.get('option')
        filter = Post.objects.all().order_by(option)
        posts = filter.filter(author=request.user)
        
        response_data = {}

        response_data = forming_dictionary(posts)
  
        return JsonResponse(response_data)

#Фильтрация по избранному - AJAX
def filter_by_favorites(request):
    if request.POST.get('action') == 'post':
        option = request.POST.get('option')
        response_data = {}

        posts = Post.objects.all().filter(author=request.user)

        if option == "True":
            posts = posts.filter(favorite=True)
        if option == "False":
            posts = posts.filter(favorite=False)
        
        posts = posts.order_by('-date')

        response_data = forming_dictionary(posts)
  
        return JsonResponse(response_data)

#Фильтрация по дате создания - AJAX
def filter_by_date(request):
    if request.POST.get('action') == 'post':
        option = request.POST.get('option')
        response_data = {}

        posts = Post.objects.all().filter(author=request.user)

        if option == "day":
            now = datetime.now() - timedelta(minutes=60*24*1)
            posts = posts.filter(date__gte=now)
        if option == "week":
            now = datetime.now() - timedelta(minutes=60*24*7)
            posts = posts.filter(date__gte=now)
        if option == "month":
            now = datetime.now() - timedelta(minutes=60*24*30)
            posts = posts.filter(date__gte=now)

        posts = posts.order_by('-date')

        response_data = forming_dictionary(posts)
  
        return JsonResponse(response_data)

#Фильтрация по категории - AJAX
def filter_by_category(request):
    if request.POST.get('action') == 'post':
        option = request.POST.get('option')
        response_data = {}

        s = Category.objects.get(title__iexact=option)
        posts = s.posts.all().filter(author=request.user)

        posts = posts.order_by('-date')

        response_data = forming_dictionary(posts)
  
        return JsonResponse(response_data)

#Поиск по заголовку - AJAX
def search_by_title(request):
    if request.POST.get('action') == 'post':
        option = request.POST.get('option')
        response_data = {}

        posts = Post.objects.filter(title__icontains=option, author=request.user)
        posts = posts.order_by('-date')

        response_data = forming_dictionary(posts)
  
        return JsonResponse(response_data)

#Удаление заметки - AJAX
def deleting_post(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        
        response_data = {}

        posts = Post.objects.get(slug__iexact = post_id)
        posts.delete()
        posts = Post.objects.all().filter(author=request.user)
        posts = posts.order_by('-date')

        response_data = forming_dictionary(posts)

        return JsonResponse(response_data)

    
