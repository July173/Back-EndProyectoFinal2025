from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.general.views.AprendizViewset import AprendizViewSet
from apps.general.views.CenterViewset import CenterViewSet
from apps.general.views.FichaViewset import FichaViewSet
from apps.general.views.InstructorViewset import InstructorViewSet
from apps.general.views.ProgramViewset import ProgramViewSet
from apps.general.views.RegionalViewset import RegionalViewSet
from apps.general.views.SedeViewset import SedeViewSet

router = DefaultRouter()
router.register(r'aprendices', AprendizViewSet, basename='aprendices')
router.register(r'centers', CenterViewSet, basename='centers')
router.register(r'fichas', FichaViewSet, basename='fichas')
router.register(r'instructors', InstructorViewSet, basename='instructors')
router.register(r'programs', ProgramViewSet, basename='programs')
router.register(r'regionals', RegionalViewSet, basename='regionals')
router.register(r'sedes', SedeViewSet, basename='sedes')

urlpatterns = [
    path('', include(router.urls)),
]
