from apps.general.repositories.TestRecordRepository import TestRecordRepository


class TestRecordService:
    def __init__(self):
        self.repository = TestRecordRepository()

    def create(self, data, db='default'):
        return self.repository.create(data, db=db)

    def list(self, db='default'):
        return self.repository.list(db=db)

    def retrieve(self, pk, db='default'):
        return self.repository.retrieve(pk, db=db)

    def update(self, pk, data, db='default'):
        return self.repository.update(pk, data, db=db)

    def delete(self, pk, db='default'):
        return self.repository.delete(pk, db=db)