from django.contrib import admin
from .entity.models import Aprendiz, Center, Ficha, Instructor, Program, Regional, Sede, AsignationInstructor, PersonSede

admin.site.register(Aprendiz)
admin.site.register(AsignationInstructor)
admin.site.register(Center)
admin.site.register(Ficha)
admin.site.register(Instructor)
admin.site.register(Program)
admin.site.register(Regional)
admin.site.register(Sede)
admin.site.register(PersonSede)
