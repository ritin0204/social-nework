from django.contrib import admin
from .models import User,Post,Follow
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id","text","created_at","likes","unlikes")

admin.site.register(User)
admin.site.register(Post,PostAdmin)
admin.site.register(Follow)