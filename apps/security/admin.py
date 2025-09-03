from django.contrib import admin
from .entity.models import User, Role, Person, Form, Permission, Module, FormModule, RolFormPermission

admin.site.register(Form)
admin.site.register(FormModule)
admin.site.register(Module)
admin.site.register(Permission)
admin.site.register(Person)
admin.site.register(RolFormPermission)
admin.site.register(Role)
admin.site.register(User)
