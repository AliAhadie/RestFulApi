from django.contrib import admin
from blog.models import Post,Category


class PostAdmin(admin.ModelAdmin):
    list_display=('author','title','status','published_date','category')


admin.site.register(Post)
admin.site.register(Category)
# Register your models here.
