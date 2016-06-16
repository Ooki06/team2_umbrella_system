from django.contrib import admin


from .models import Room,Genre,User,Order

admin.site.register(Room)
admin.site.register(Genre)
admin.site.register(User)
admin.site.register(Order)

# Register your models here.