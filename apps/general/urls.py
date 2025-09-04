from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.general.views.AprendizViewset import AprendizViewset
from apps.general.views.CenterViewset import CenterViewset
from apps.general.views.FichaViewset import FichaViewset
from apps.general.views.InstructorViewset import InstructorViewset
from apps.general.views.ProgramViewset import ProgramViewset
from apps.general.views.RegionalViewset import RegionalViewset
from apps.general.views.SedeViewset import SedeViewset
from apps.general.views.PersonSedeViewset import PersonSedeViewset
from apps.general.views.CreateInstructorViewset import CreateInstructorViewset
from apps.general.views.KnowledgeAreaViewset import KnowledgeAreaViewset
from apps.general.views.CreateAprendizViewset import CreateAprendizViewset


router = DefaultRouter()
router.register(r'aprendices', AprendizViewset, basename='general_aprendices')
router.register(r'centers', CenterViewset, basename='general_centers')
router.register(r'fichas', FichaViewset, basename='general_fichas')
router.register(r'instructors', InstructorViewset, basename='general_instructors')
router.register(r'programs', ProgramViewset, basename='general_programs')
router.register(r'regionals', RegionalViewset, basename='general_regionals')
router.register(r'sedes', SedeViewset, basename='general_sedes')
router.register(r'person-sedes', PersonSedeViewset, basename='general_person_sedes')
router.register(r'create-instructors', CreateInstructorViewset, basename='general_create_instructors')
router.register(r'knowledge-areas', KnowledgeAreaViewset, basename='general_knowledge_areas')
router.register(r'create-aprendices', CreateAprendizViewset, basename='general_create_aprendices')

urlpatterns = [
    path('', include(router.urls)),
]
