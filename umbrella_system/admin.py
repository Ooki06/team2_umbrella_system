from django.contrib import admin


from .models import Room,Genre,User,Order,Holiday

class OrderAdmin(admin.ModelAdmin):
    list_display = ('room','order_day','time_zone_id','genre','charge_lv','user')
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name','seats')
admin.site.register(Room,RoomAdmin)
admin.site.register(Genre)
admin.site.register(User)
admin.site.register(Holiday)
admin.site.register(Order,OrderAdmin)

# Register your models here.