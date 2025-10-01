from django.contrib import admin
from .entity.models import Aprendiz, Center, Ficha, Instructor, Program, Regional, Sede, PersonSede, KnowledgeArea, Colors, TypeOfQueries, SupportSchedule, SupportContact, LegalDocument, LegalSection

admin.site.register(Aprendiz)
admin.site.register(Center)
admin.site.register(Ficha)
admin.site.register(Instructor)
admin.site.register(Program)
admin.site.register(Regional)
admin.site.register(Sede)
admin.site.register(PersonSede)
admin.site.register(KnowledgeArea)
admin.site.register(Colors)
admin.site.register(TypeOfQueries)
admin.site.register(SupportSchedule)
admin.site.register(SupportContact)
admin.site.register(LegalDocument)
admin.site.register(LegalSection)
