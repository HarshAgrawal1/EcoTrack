from django.contrib import admin

# Register your models here.
from registration.models import Registration
from registration.models import Additem
from registration.models import OrderDetail
# from home.models import UserBookData

admin.site.register(Registration)
admin.site.register(Additem)
admin.site.register(OrderDetail)
# admin.site.register(UserBookData)
