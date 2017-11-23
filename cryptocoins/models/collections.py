from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Collections(BaseModel):
    created_at = DateTimeField()
    name = TextField(index=True)
    url = TextField()

    class Meta:
        db_table = 'collections'
