from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.assign.views.EnterpriseViewset import EnterpriseViewset
from apps.assign.views.BossViewset import BossViewset
from apps.assign.views.HumanTalentViewset import HumanTalentViewset
from apps.assign.views.ModalityProductiveStageViewset import ModalityProductiveStageViewset
from apps.assign.views.RequestAsignationViewset import RequestAsignationViewset
from apps.assign.views.AsignationInstructorViewset import AsignationInstructorViewset
from apps.assign.views.VisitFollowingViewset import VisitFollowingViewset
from apps.assign.views.FormRequestViewset import FormRequestAPIView

router = DefaultRouter()
router.register(r'empresas', EnterpriseViewset, basename='assign_empresas')
router.register(r'jefes', BossViewset, basename='assign_jefes')
router.register(r'talento-humano', HumanTalentViewset, basename='assign_talento_humano')
router.register(r'modalidades-etapa-productiva', ModalityProductiveStageViewset, basename='assign_modalidades_etapa_productiva')
router.register(r'solicitudes-asignacion', RequestAsignationViewset, basename='assign_solicitudes_asignacion')
router.register(r'asignaciones-instructor', AsignationInstructorViewset, basename='assign_asignaciones_instructor')
router.register(r'visitas-seguimiento', VisitFollowingViewset, basename='assign_visitas_seguimiento')
# FormRequestViewset ya no se registra en el router porque es APIView

urlpatterns = [
    path('', include(router.urls)),
    path('form-requests/', FormRequestAPIView.as_view(), name='form_requests'),
]
