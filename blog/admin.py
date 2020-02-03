from django.contrib import admin
from .models import post,Chanel,Comment,is_author

admin.site.register(post)
admin.site.register(Chanel)
admin.site.register(Comment)
admin.site.register(is_author)
