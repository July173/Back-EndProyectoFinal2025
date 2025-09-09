from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.FormModuleRepository import FormModuleRepository


class FormModuleService(BaseService):

    def update_module_with_forms(self, pk, data):
        """
        Actualiza un módulo y sus formularios asociados.
        data: { 'name': str, 'description': str, 'form_ids': [int, ...] }
        """
        from apps.security.entity.models import Module, Form, FormModule
        module = Module.objects.get(pk=pk)
        module.name = data['name']
        module.description = data.get('description', '')
        module.save()
        # Eliminar asociaciones actuales
        FormModule.objects.filter(module=module).delete()
        created = 0
        for form_id in data['form_ids']:
            form = Form.objects.get(pk=form_id)
            FormModule.objects.create(form=form, module=module)
            created += 1
        return {
            'module_id': module.id,
            'forms_updated': created
        }
    def create_module_with_forms(self, data):
        """
        Crea un módulo y asocia múltiples formularios (crea registros en FormModule).
        data: { 'name': str, 'description': str, 'form_ids': [int, ...] }
        """
        from apps.security.entity.models import Module, Form, FormModule
        module = Module.objects.create(
            name=data['name'],
            description=data.get('description', '')
        )
        created = 0
        for form_id in data['form_ids']:
            form = Form.objects.get(pk=form_id)
            FormModule.objects.create(form=form, module=module)
            created += 1
        return {
            'module_id': module.id,
            'forms_added': created
        }
    def __init__(self):
        self.repository = FormModuleRepository()
