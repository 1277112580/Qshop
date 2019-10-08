from django.db import models

# Create your models here.
# 用户表
class LoginUser(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=32)
    username=models.CharField(max_length=32,null=True,blank=True)
    pthone_number=models.CharField(max_length=11,null=True,blank=True)
    photo=models.ImageField(upload_to='img',null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    gender=models.CharField(null=True,blank=True,max_length=8)
    address=models.TextField(null=True,blank=True)
    user_type=models.IntegerField(default=1)#0代表卖家， 1代表买家，2代表管理员

#商品类型
class GoodsType(models.Model):
    type_label=models.CharField(max_length=32)
    type_description=models.TextField()
    type_picture=models.ImageField(upload_to='images')

# 商品表
class Goods(models.Model):
    goods_number=models.CharField(max_length=11)
    goods_name=models.CharField(max_length=32)
    goods_price=models.FloatField()
    goods_count=models.IntegerField()
    goods_location=models.CharField(max_length=254)
    goods_safe_date=models.IntegerField()
    goods_status = models.IntegerField(default=1)  # 0代表下架  1代表在售
    goods_pro_time=models.DateField(auto_now=True,verbose_name='生产日期')
    picture = models.ImageField(upload_to="images")
    goods_description=models.TextField(default='味美价廉')
    ## 类型  一对多
    goods_type=models.ForeignKey(to=GoodsType,on_delete=models.CASCADE,default=1)
    ## 店铺 一对多
    goods_store=models.ForeignKey(to=LoginUser,on_delete=models.CASCADE,default=1)








