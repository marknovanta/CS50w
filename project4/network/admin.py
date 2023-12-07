from django.contrib import admin
from network.models import Post, Follow, User

# Register your models here.
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(User)