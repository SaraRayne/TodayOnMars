from django.contrib import admin
from .models import User, Thread, Category, Reply
# Register your models here.

class ThreadAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

# Register your models here.
admin.site.register(User)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Category)
admin.site.register(Reply)
