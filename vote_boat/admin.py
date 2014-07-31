from django.contrib import admin

from django.contrib import admin
from .models import Poll,Idea,User


admin.site.register(Poll)
admin.site.register(Idea)
admin.site.register(User)
