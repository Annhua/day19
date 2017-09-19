from django.shortcuts import render, redirect,HttpResponse
from blog.models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
# Create your views here.
import json

def index(request):
    author_list = Author.objects.all()
    publish_list = Publish.objects.all()
    classes_list = Classfication.objects.all()

    if request.method == "POST":

        title = request.POST.get('title')
        price = request.POST.get('price')
        author = request.POST.getlist('authors')
        publish = request.POST.get('publish')
        classify = request.POST.get('classes')
        book = Book.objects.create(title=title, price=price, publisher_id=publish,
                                   classes_id=classify)
        book.authors.add(*Author.objects.filter(id__in=author))
        return redirect('/add/')
    return render(request, 'get.html', locals())
    #     return redirect('/get/')


def add(request):

    book_list=Book.objects.all()
    p_obj = Paginator(book_list,4)
    obj_num = request.GET.get('page')
    try:
        list_all = p_obj.page(obj_num)
    except EmptyPage:
        list_all = p_obj.page(p_obj.num_pages)
    except PageNotAnInteger:
        list_all = p_obj.page(1)

    if request.user.is_authenticated():
        return render(request, 'add.html', locals())
    else:
        return render(request,'foo.html')


def dele(request):
    id = request.GET.get('id')
    obj = Book.objects.filter(id=id).delete()
    return HttpResponse(json.dumps(obj))


def edit(request,id):
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()
    classes_list = Classfication.objects.all()
    book_list= Book.objects.filter(id=id).first()
    if request.method=='POST':
        id=request.POST.get('id')
        title = request.POST.get('title')
        price = request.POST.get('price')
        publish = request.POST.get('publish')
        classes = request.POST.get('classes')
        authors = request.POST.getlist('authors[]')
        # print('+++++++++++++++++++++++++++++++++++++++++++++')
        Book.objects.filter(id=id).update(title=title,price=price,publisher_id=publish,classes_id=classes)
        # print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        book_id=Book.objects.filter(id=id).first()
        book_id.authors.remove(*Author.objects.all())
        book_id.authors.add(*authors)
        print(title,price,authors,publish)
        return redirect('/add/')
    return render(request,'edit.html',locals())


def delet(request):
    id = request.GET.get('id')
    obj = Book.objects.filter(id=id).delete()
    return HttpResponse(json.dumps(obj))



def foo(request):
    errpr='输入错误'
    if request.method=='POST':
        user=request.POST.get('username')
        pwd=request.POST.get('password')
        user_new=auth.authenticate(username=user,password=pwd)
        if user_new:
            auth.login(request,user_new)
            return redirect('/add/')
        else:
            return render(request,'foo.html',{'errpr':errpr})



    return render(request,'foo.html')

def zhuce(request):
    err=''
    if request.method=='POST':
        user=request.POST.get('username',None)
        pwd=request.POST.get('password',None)
        pwd_q = request.POST.get('new_password',None)
        if not user:
            err='用户名不能为空'
        elif not pwd or not pwd_q:
            err='密码不能为空'
        elif pwd !=pwd_q:
            err='密码输入不一致'
        elif User.objects.filter(username=user):
            err='用户名存在'
        else:
            User.objects.create_user(username=user,password=pwd)
            return redirect('/foo/')


    return render(request,'zhuce.html',{'err':err})
@login_required
def zhuxiao(request):
    auth.logout(request)
    return redirect('/foo/')

@login_required
def xiugaimima(request):
    user=request.user
    errpr=''
    if request.method=='POST':
        pwd = request.POST.get('password')
        pwd_1 = request.POST.get('new_password')
        pwd_2 = request.POST.get('new2_password')
        if user.check_password(pwd):
            if not pwd_1:
                errpr='请重新输入'
            elif pwd_1 != pwd_2:
                errpr='密码输入不一致'
            else:
                user.set_password(pwd_1)
                user.save()
                errpr='密码修改成功'
                return render(request, 'foo.html', {'errpr': errpr})
    else:
        errpr='密码错误'
    return render(request,'mima.html',{'errpr': errpr})
