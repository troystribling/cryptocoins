from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, BooleanField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Collections(BaseModel):
    created_at = DateTimeField()
    path = TextField(index=True)
    success = BooleanField()
    url = TextField()

    class Meta:
        db_table = 'collections'
        indexes = (
            (('created_at', 'path'), True),
        )

    @classmethod
    def create_collection(cls, path, url):
        try:
            with database.atomic():
                return cls.create(path=path, url=url)
        except IntegrityError:
            print(f"ERROR COLLECTION EXISTS: {path}, {created_at}")
            return None

    def collection_successful(self):
        query = Collections.update(success=True).where(Collections.created_at == self.created_at & Collections.path == self.path)
        query.execute()
