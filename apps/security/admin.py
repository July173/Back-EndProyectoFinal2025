from django.contrib import admin
from .models import User, Role, Person, Form, Permission, Module, FormModule, RolFormPermission

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Person)
admin.site.register(Form)
admin.site.register(Permission)
admin.site.register(Module)
admin.site.register(FormModule)
admin.site.register(RolFormPermission)
