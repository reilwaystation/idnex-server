from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Ticket, Token


class BaseUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser',)
    fieldsets = ((None,
                  {'fields': [
                      'email',
                      'username',
                      'first_name',
                      'last_name',
                      'password',
                      'is_superuser',
                      'is_staff',
                      'is_active',
                      'thumbnail'
                  ]}),
                 )
    add_fieldsets = ((None,
                      {'fields': [
                          'email',
                          'username',
                          'first_name',
                          'last_name',
                          'password1',
                          'password2',
                          'is_superuser',
                          'is_staff',
                          'is_active',
                          'thumbnail'
                      ]}),
                     )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Token)
admin.site.register(Ticket)
admin.site.register(User, BaseUserAdmin)
admin.site.unregister(Group)
