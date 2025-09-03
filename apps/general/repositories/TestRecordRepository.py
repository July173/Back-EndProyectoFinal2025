from apps.general.entity.models import TestRecord


class TestRecordRepository:
    def create(self, data, db='default'):
        data = dict(data)  # Asegúrate de que sea un dict mutable
        data.pop('db', None)  # Elimina 'db' si existe
        return TestRecord.objects.using(db).create(**data)

    def list(self, db='default'):
        return TestRecord.objects.using(db).all()

    def retrieve(self, pk, db='default'):
        return TestRecord.objects.using(db).get(pk=pk)

    def update(self, pk, data, db='default'):
        data = dict(data)
        data.pop('db', None)
        obj = TestRecord.objects.using(db).get(pk=pk)
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save(using=db)
        return obj

    def delete(self, pk, db='default'):
        obj = TestRecord.objects.using(db).get(pk=pk)
        obj.delete(using=db)
        return obj