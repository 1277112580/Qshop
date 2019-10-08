from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import hashlib
from Saller.models import *
from Buyer.models import *
# Create your views here.

# 主页
def index(request):
    goods_type=GoodsType.objects.all()
    result=[]
    for type in goods_type:
        goods=type.goods_set.order_by('-goods_price')
        if len(goods)>= 4:
            goods=goods[:4]
            result.append({'type':type,'goods':goods})
    # print(goods)
    return render(request,'buyer/index.html',locals())

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
            return HttpResponseRedirect('/Buyer/login/')
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
                user.save()
            else:
                error_msg='邮箱已存在，请输入新的邮箱'
        else:
            error_msg='邮箱不能为空'
    return render(request,'buyer/register.html',locals())


# 登录
def login(request):
    if request.method=="POST":
        error_msg=''
        ##获取值
        email=request.POST.get('email')
        password=request.POST.get('password')
        # 如果用户输入了email
        if email:
            #是实例化一个用户
            user=LoginUser.objects.filter(email=email,user_type=1).first()
            # 用户存在
            if user:
                # 密码相等
                if user.password==setPassword(password):
                   # #跳转页面
                    response=HttpResponseRedirect('/Buyer/index/')
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
    return render(request,"buyer/login.html",locals())

# 退出
def logout(request):
    # 删除cookie  删除session
    response=HttpResponseRedirect('/Buyer/login/')
    keys=request.COOKIES.keys()
    for i in keys:
        response.delete_cookie(i)

    # del response.session['username']
    return response

# 模板
def base(requset):
    return render(requset,'Buyer/base.html')

# 商品列表
def goods_list(request):
    """
    根据keywords传递的类型id 寻找该类型下面的商品
    req_type 完成判断请求
        当req_type==search
            kerwords 传递商品的名字
        当req_type==findeall
            keywords 传递的类型id 寻找该类型下面的商品
            
    :param request: 
    :return: 
    """
    keywords=request.GET.get('keywords')
    req_type=request.GET.get('req_type')
    if req_type=='findall':
        # 查看更多
        goods_type=GoodsType.objects.get(id=keywords)
        goods=goods_type.goods_set.all() #反向查询
    elif req_type=='search':
        ###搜索功能
        goods=Goods.objects.filter(goods_name__contains=keywords).all()

    end=len(goods)//5
    end+=1
    recommend=goods.order_by('-goods_pro_time')[:end]
    return render(request,'buyer/goods_list.html',locals())

#商品详情
def detail(request,id):
    goods=Goods.objects.get(id=int(id))
    goodstype=Goods.objects.filter(goods_type=goods.goods_type).all()
    recommend=goodstype.order_by('-goods_pro_time')[:2]
    return render(request,'buyer/detail.html',locals())

# 个人中心
@LoginVaild
def user_center_info(request):
    return render(request,'buyer/user_center_info.html',locals())

import time
# 订单页面
@LoginVaild
def place_order(request):
    goods_id=request.GET.get('goods_id') #商品id
    goods_count=request.GET.get('goods_count') #商品数量
    user_id=request.COOKIES.get('userid')
    # print(goods_id)
    if goods_count and goods_id:
        goods_id=int(goods_id)
        goods_count=int(goods_count)
        goods = Goods.objects.get(id=goods_id)
    #     保存订单
        payorder=PayOrder()
        order_number=str(time.time()).replace('.','')
        payorder.order_number=order_number
        payorder.order_status=0
        payorder.order_total=goods.goods_price* goods_count
        payorder.order_user=LoginUser.objects.get(id=user_id)
        payorder.save()
        #保存订单详情表
        orderinfo=OrderInfo()
        orderinfo.order_id=payorder
        orderinfo.goods=goods
        orderinfo.goods_count = goods_count
        orderinfo.goods_price=goods.goods_price
        orderinfo.goods_total_price=goods.goods_price*goods_count
        orderinfo.store_id=goods.goods_store
        orderinfo.save()

        total_count=0
        all_goods_info=payorder.orderinfo_set.all()
        for one in all_goods_info:
            total_count+=one.goods_count
    return render(request,'buyer/place_order.html',locals())


from alipay import AliPay
from Qshop.settings import alipay_public_key_string,alipay_private_key_string
# ali支付
def AlipayViews(request):

    order_id=request.GET.get('order_id')
    payorder=PayOrder.objects.get(id=order_id)
    # 实例化对象
    alipay=AliPay(
            appid="2016101300673947",
            app_notify_url=None,
            app_private_key_string=alipay_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",

    )

    # 实例化订单
    order_string=alipay.api_alipay_trade_page_pay(
        subject='天天生鲜',  #交易主体
        out_trade_no=payorder.order_number, #订单号
        total_amount=str(payorder.order_total),  #交易总金额
        return_url="http://127.0.0.1:8000/Buyer/payresult",      #请求支付，之后及时回调的一个接口
        notify_url="http://127.0.0.1:8000/Buyer/payresult",      #通知地址
    )

    # 发送支付请求
    # 请求地址  支付网关+实例化订单
    result='https://openapi.alipaydev.com/gateway.do?'+order_string
    print(result)

    return HttpResponseRedirect(result)

# 支付结果
def payresult(request):


    data=request.GET
    # 通过get获取支付宝传递参数，获取其中的订单号；修改订单的状态
    order_number=request.GET.get('out_trade_no')
    payorder=PayOrder.objects.get(order_number=order_number)
    payorder.order_status=1
    payorder.save()
    print(data)

# 购物车
@LoginVaild
def cart(request):
    user_id=request.COOKIES.get('userid')
    # 查询购物车中的商品
    cart_list=[]
    cart=Cart.objects.filter(cart_user_id=user_id,).order_by('-id')
    count=cart.count()  #获取条数 10
    for one in cart:
        if one.order_number !='0':
    #         说明有订单 号 订单状态不为 已支付
            payorder=PayOrder.objects.get(order_number=one.order_number)
            if payorder.order_status !=1:
                ##已支付的订单
                cart_list.append(one)
            else:
                count-=1
        else:
            cart_list.append(one)
    return render(request,"buyer/cart.html",locals())

# 添加购物车
@LoginVaild
def add_cart(requset):
    """
    使用post请求，完成添加购物车功能
    :param requset:   
    :return: json code msg
    get("key",None) 
    """

    result = {'code': 200, 'msg':""}
    if requset.method=="POST":
        goods_id=requset.POST.get('goods_id')
        count=float(requset.POST.get('count',1))
        user_id=requset.COOKIES.get('userid')
        goods=Goods.objects.get(id=goods_id)
        # 保存购物车
        cart=Cart()
        cart.goods_number=count
        cart.goods_price=goods.goods_price
        cart.goods_total=cart.goods_price*count
        cart.goods=goods
        cart.cart_user=LoginUser.objects.get(id=user_id)
        cart.save()
        result['code']=1000
        result['msg']='添加商品成功'
    else:
        result['code'] = 1001
        result['msg'] = '请求方式不对'

    return JsonResponse(result)

# 多笔订单
@LoginVaild
def place_oeder_more(request):
    data=request.GET
    userid=request.COOKIES.get('userid')
    #<QueryDict: {'goods_2_19': ['on'], 'count_1': ['1'], 'count_2': ['3'], 'count_16': ['1']}>
    print(data)
    # 区分 通过获取前端get请求的参数，找到goods_id 和对应的数量
    # startwith  以goods开始的key
    data_item=data.items()
    # print(data_item) #<generator object MultiValueDict.items at 0x00000000052EB0F8>
    request_data=[]
    for key,value in data_item:
        print("%s--------%s"%(key,value))  #key
        if key.startswith('goods'):
            goods_id=key.split('_')[1]
            # print(goods_id)
            count=request.GET.get('count_'+goods_id)
            cart_id=key.split('_')[2]
            # print('%s++++%s'%(cart_id))
            request_data.append((int(goods_id),int(count),int(cart_id)))
    print(request_data)
    if request_data:
        #保存数据
        #保存一笔订单表 订单详情表
        payorder=PayOrder()
        order_number=str(time.time()).replace('.','') ##生产订单编号
        payorder.order_number=order_number  #订单编号
        payorder.order_status=0  #商品状态 0未支付  1已支付
        payorder.order_total=0
        payorder.order_user=LoginUser.objects.get(id=userid)
        payorder.save()
        order_total=0   #初始订单总价为零
        total_count=0   #初始商品总数量
        #订单详情 保存多条，一种商品一条数据
        for goods_id_one,count_one,cart_id in request_data:
            #遍历到一条订单中的多条商品的id 和对应的数量
            goods=Goods.objects.get(id=goods_id_one)
            orderinfo=OrderInfo()
            orderinfo.order_id=payorder
            orderinfo.goods=goods
            orderinfo.goods_count=count_one
            orderinfo.goods_price=goods.goods_price
            orderinfo.goods_total_price=goods.goods_price*count_one
            orderinfo.store_id=goods.goods_store
            orderinfo.save()
            order_total+=goods.goods_price*count_one
            total_count+=count_one

            cart=Cart.objects.get(id=cart_id)
            cart.order_number=order_number
            cart.save()

        payorder.order_total=order_total
        payorder.save()

    return render(request,'buyer/place_order.html',locals())



# 全部订单
@LoginVaild
def user_center_order(request):
    user_id=request.COOKIES.get('userid')
    # 通过用户  获取该用户所有订单
    user=LoginUser.objects.get(id=user_id)
    payorder=user.payorder_set.order_by('-order_date','order_status')
    return render(request,"buyer/user_center_order.html",locals())




