from django.shortcuts import render, redirect, HttpResponse
from app01 import models
# Create your views here.

def publisher_list(request):
    # 逻辑
    # 获取所有的出版社信息
    all_publishers = models.Publisher.objects.all().order_by('id') #对象列表
    for i in all_publishers:
        print(i)
        print(i.name)
        print(i.id)

    # 返回一个页面
    return render(request, 'publisher_list.html', {'all_publishers': all_publishers})

# 新增一个出版社
def publisher_add(request):
    if request.method == 'POST':
        # post请求，获取用户提交的数据，
        pub_name = request.POST.get('pub_name')
        print(pub_name)
        if not pub_name:
            # 输入为空
            return render(request, 'publisher_add.html', {'error': '出版社名字不能为空'})
        if models.Publisher.objects.filter(name=pub_name):
            # 数据库中有重复的名字了
            return render(request, 'publisher_add.html', {'error': '出版社名称已存在'})
        # 将数据新增到数据库，
        ret = models.Publisher.objects.create(name=pub_name)
        # get请求返回一个页面，页面中包含form表单
        return redirect('/publisher_list/')

    return render(request, 'publisher_add.html')

# 删除出版社
def publisher_del(request):
    # 获取要删除数据的id
    pk = request.GET.get('pk')
    # 根据id到数据库进行删除
    models.Publisher.objects.filter(pk=pk).delete() #查询到一个对象列表 删除该列表中的所有对象
    # 返回重定向到展示出版社的页面
    return redirect('/publisher_list/')

def publisher_edit(request):
    pk = request.GET.get('pk')
    pub_obj = models.Publisher.objects.get(pk=pk)

    if request.method == 'GET':
        # get 返回一个页面，包含form表单 input原始数据
        return render(request, 'publisher_edit.html', {'pub_obj': pub_obj})
    else:
        #  post
        # 获取用户要提交的出版社名称
        pub_name = request.POST.get('pub_name')
        if not pub_name:
            # 输入为空
            return render(request, 'publisher_edit.html', {'error': '出版社名字不能为空'})
        # 修改数据库中的数据
        pub_obj.name = pub_name #只是在内存中修改了
        pub_obj.save() #将修改操作提交至数据库
        # 返回重定向到展示出版社的页面
        return redirect('/publisher_list/')

# 展示书籍
def book_list(request):
    # 查询所有书籍
    all_books = models.Book.objects.all()
    # for book in all_books:
    #     print(book)
    #     print(book.pk)
    #     print(book.name)
    #     print(book.name)
    #     print(book.publisher, book.publisher.pk, book.publisher.name)
    # 返回一个页面，页面包含书籍数据
    return render(request, 'book_list.html', {'all_books': all_books})

# 新增书籍
def book_add(request):
    error = ''
    if request.method == 'POST':
        # 获取用户提交的数据
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')

        if not book_name:
            # 用户输入名称为空
            error = '书名不能为空'
        elif models.Book.objects.filter(name=book_name):
            error = '书名不能重复'
        else:
            # 将数据迁移到数据库
            models.Book.objects.create(name=book_name, publisher_id=pub_id)
            # 返回重定向页面
            return redirect('/book_list/')
        # 查询所有出版社
        all_publishers = models.Publisher.objects.all()
        return render(request, 'book_add.html', {'all_publishers': all_publishers, 'error': error})



    # 查询所有出版社
    all_publishers = models.Publisher.objects.all()
    # get返回一个form表单页面
    return render(request, 'book_add.html', {'all_publishers': all_publishers})

# 删除图书
def book_del(request):
    # 获取用户提交的要删除数据的id
    pk = request.GET.get('id')
    # 获取要删除的对象，删除
    models.Book.objects.filter(pk=pk).delete()
    # 返回一个重定向的页面
    return redirect('/book_list/')

def book_edit(request):
    # 查询要编辑对象的id
    pk = request.GET.get('id')
    # 根据id查到要编辑的对象
    book_obj = models.Book.objects.get(pk=pk)

    # post请求
    if request.method == 'POST':
        # 获取到用户新提交的数据
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        # 编辑对象修改
        # book_obj.name = book_name
        # book_obj.publisher_id = pub_id
        # 保存到数据库
        # book_obj.save()
        # 方法二
        models.Book.objects.filter(pk=pk).update(name=book_name, publisher_id=pub_id)
        # 重定向展示页面
        return redirect('/book_list/')

    # get请求

    # 返回一个页面 包含原始数据
    all_publishers =models.Publisher.objects.all()
    return render(request, 'book_edit.html', {'book_obj': book_obj, 'all_publishers': all_publishers})

def author_list(request):
    # 查询所有作者
    all_authors = models.Author.objects.all()
    # for book in all_books:
    #     print(book)
    #     print(book.pk)
    #     print(book.name)
    #     print(book.name)
    #     print(book.publisher, book.publisher.pk, book.publisher.name)
    # 返回一个页面，页面包含书籍数据
    return render(request, 'author_list.html', {'all_authors': all_authors})

def author_add(request):
    error = ''
    if request.method =='POST':
        # 获取用户提交的数据
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')  #用getlist获取多个数据
        # 向数据库中插入数据
        # 向作者表插入了作者信息
        author_obj = models.Author.objects.create(name=author_name)
        # 该作者和对应的书籍绑定多对多的关系
        author_obj.books.set(book_ids)  #设置多对多关系
        # 返回重定向到展示作者页面
        return redirect('/author_list/')

    # 查询所有的书籍
    all_books = models.Book.objects.all()

    # 返回一个页面，包含form表单，让用户输入作者姓名，选择作品
    return render(request, 'author_add.html', {'all_books': all_books})

def author_del(request):
    # 获取用户提交的要删除数据的id
    pk = request.GET.get('id')
    # 获取要删除的对象，删除
    models.Author.objects.filter(pk=pk).delete()

    # 返回一个重定向的页面
    return redirect('/author_list/')

def author_edit(request):
    # 获取要编辑对象的id
    pk = request.GET.get('id')
    # 根据id获取作者对象
    author_obj = models.Author.objects.get(pk=pk)

    # post
    if request.method == 'POST':
        # 获取用户新提交的数据
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')
        # 修改作者姓名
        author_obj.name = author_name
        author_obj.save()
        # 修改作者和书多对多的关系
        author_obj.books.set(book_ids)
        # 返回重定向页面
        return redirect('/author_list/')

    # get
    # 获取所有书籍
    all_books = models.Book.objects.all()
    # 返回一个页面，页面中包含作者的姓名，代表作
    return render(request, 'author_edit.html', {'author_obj': author_obj, 'all_books': all_books})