from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.UserRepository import UserRepository
from django.contrib.auth.hashers import make_password


class UserService(BaseService):
    def __init__(self):
        self.repository = UserRepository()

    def create(self, data):
        pwd = data.get('password')
        if pwd:
            data['password'] = make_password(pwd)
        return super().create(data)

    def change_password(self, pk, new_password):
        inst = self.get(pk)
        inst.set_password(new_password)
        inst.save()
        return inst
