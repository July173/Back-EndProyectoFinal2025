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
from apps.general.views.KnowledgeAreaViewset import KnowledgeAreaViewset
from apps.general.views.ColorsViewset import ColorsViewset
from apps.general.views.TypeOfQueriesViewset import TypeOfQueriesViewset
from apps.general.views.SupportScheduleViewset import SupportScheduleViewset

router = DefaultRouter()
router.register(r'aprendices', AprendizViewset, basename='general_aprendices')
router.register(r'centers', CenterViewset, basename='general_centers')
router.register(r'fichas', FichaViewset, basename='general_fichas')
router.register(r'instructors', InstructorViewset, basename='general_instructors')
router.register(r'programs', ProgramViewset, basename='general_programs')
router.register(r'regionals', RegionalViewset, basename='general_regionals')
router.register(r'sedes', SedeViewset, basename='general_sedes')
router.register(r'person-sedes', PersonSedeViewset, basename='general_person_sedes')
router.register(r'knowledge-areas', KnowledgeAreaViewset, basename='general_knowledge_areas')
router.register(r'colors', ColorsViewset, basename='general_colors')
router.register(r'type-of-queries', TypeOfQueriesViewset, basename='general_type_of_queries')
router.register(r'support-schedules', SupportScheduleViewset, basename='general_support_schedules')


urlpatterns = [
    path('', include(router.urls)),
]
