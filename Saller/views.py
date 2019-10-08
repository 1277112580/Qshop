from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from Saller.models import *
import hashlib
from django.core.paginator import Paginator
# Create your views here.

# 装饰器
def LoginVaild(func):
    ##1.获取cookie中的username和eamil
    ##2.判断username和eamil
    ##3. 如果成功 跳转
    ##4. 如果失败 login.html
    def inner(request,*args,**kwargs):
        # 获取cookie
        username=request.COOKIES.get('username')
        #获取session
        session_username = request.session.get("username")
        # 三个条件都成立
        if username and session_username and username==session_username:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Saller/login/')
    return inner

# 加密
def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

# 注册
def register(request):
    if request.method=="POST":
        error_msg=''
        email=request.POST.get('email')
        password=request.POST.get('password')
        if email:
            ##判断邮箱是否存在
            loginuser=LoginUser.objects.filter(email=email).first()
            if not loginuser:
                ##不存在写库
                user=LoginUser()
                user.email=email
                user.username=email
                # 将密码加密进行保存
                user.password=setPassword(password)
                user.user_type=0
                user.save()
            else:
                error_msg='邮箱已存在，请输入新的邮箱'
        else:
            error_msg='邮箱不能为空'
    return render(request,'seller/register.html',locals())

# 登录
def login(request):
    if request.method=="POST":
        error_msg=''
        ##获取值
        email=request.POST.get('email')
        password=request.POST.get('password')
        # 如果用户输入了email
        if email:
            #实例化一个用户
            user=LoginUser.objects.filter(email=email,user_type=0).first()
            # 用户存在
            if user:
                # 密码相等
                if user.password==setPassword(password):
                   # #跳转页面
                    response=HttpResponseRedirect('/Saller/index/')
                    ##设置cookie
                    response.set_cookie('email',user.email)
                    response.set_cookie('username',user.username)
                    response.set_cookie('userid',user.id)
                    request.session['username']=user.username #设置session
                    return response
                else:
                    error_msg='密码错误'
            else:
                error_msg='用户不存在'
        else:
            error_msg='登录邮箱不能为空'
    return render(request,"seller/login.html",locals())

# 主页
@LoginVaild
def index(request):
    # username=request.COOKIES.get('username')
    return render(request,'seller/index.html')

# 登出
def logout(request):
    # 删除cookie  删除session
    response=HttpResponseRedirect('/Saller/login/')
    keys=request.COOKIES.keys()
    for i in keys:
        response.delete_cookie(i)

    del request.session['username']
    return response

# 商品列表分页
def goods_list(request,status,page=1):
    page=int(page)
    if status=="0":
        #下架商品
        goods_obj=Goods.objects.filter(goods_status=0).order_by('goods_number') #返回一个商品对象
    else:
        #在售商品
        goods_obj=Goods.objects.filter(goods_status=1).order_by('goods_number')
    paginator=Paginator(goods_obj,10) #每页显示十条数据
    page_obj=paginator.page(page)
    nowpage=page_obj.number
    start=nowpage-2
    end=nowpage+2
    page_range=paginator.page_range[start:end]
    # print(page)
    return render(request,'seller/goods_list.html',locals())

# 商品销售状态
def goods_status(request,status,id):
    id=int(id)
    goods=Goods.objects.get(id=id)
        #上架
    if status=='up':
        goods.goods_status=1
    else:
        #下架
        goods.goods_status=0
    goods.save()
    #获取请求来源
    url=request.META.get("HTTP_REFERER","/Saller//goods_list/1/1")
    return HttpResponseRedirect(url)

@LoginVaild
# 个人中心
def personal_info(request):
    user_id = request.COOKIES.get('userid')
    print(user_id)
    user = LoginUser.objects.filter(id=user_id).first()
    if request.method == "POST":
        data = request.POST
        print(data.get('email'))
        user.username = data.get('username')
        user.phone_number = data.get('phone_number')
        user.age = data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        user.photo = request.FILES.get("photo")
        user.save()
        print(data)
    return render(request,'seller/personal_info.html',locals())

@LoginVaild
# 增加商品
def goods_add(request):
    # 处理post请求，获取数据，保存数据，返回响应
    goods_type=GoodsType.objects.all()
    if request.method=="POST":
        data=request.POST
        print(data)
        goods=Goods()
        goods.goods_number=data.get('goods_number')
        goods.goods_name=data.get('goods_name')
        goods.goods_price=data.get('goods_price')
        goods.goods_count=data.get('goods_count')
        goods.goods_location=data.get('goods_location')
        goods.goods_safe_date=data.get('goods_safe_date')
        goods.picture=request.FILES.get('picture')
        goods.goods_status = 1
        goods.save()
        # 获取用户提交的商品类型    进行保存
        goods_type=request.POST.get('goods_type')
        goods.goods_type=GoodsType.objects.get(id=goods_type) #保存类型
        #select 标签的类型为string类型

        # 从cookie中获取用户信息    保存店铺
        user_id=request.COOKIES.get('userid')
        goods.goods_store=LoginUser.objects.get(id=user_id)
        goods.save()
    return render(request,'seller/goods_add.html',locals())