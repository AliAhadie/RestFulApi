from django.contrib import admin
from django import forms
from accounts.models import User,Profile
from blog.models import Post,Category
from django.contrib.auth.admin import UserAdmin


"""coustom user admin panel for show inharit with UserAdmin"""

class CoustomUserAdmin(UserAdmin):
    model=User
    list_display = ('email' , 'is_superuser','is_active')
    searching_fields=('email',)
    ordering=('email',)
    fieldsets = (
        ('Authentication', {"fields": ("email", "password")}),

        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", )}),
    )
    add_fieldsets=(
        (None,
         {'classes':('wide',),
          'fields':('email','password1','password2','is_staff','is_active','is_superuser',)
          }
          ),
    )    
"""adding to admin panel """    

admin.site.register(User,CoustomUserAdmin)
admin.site.register(Profile)


