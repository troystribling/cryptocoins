from peewee import Model, PostgresqlDatabase, DateTimeField, TextField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Imports(BaseModel):
    created_at = DateTimeField()
    remote_path = TextField(null=True, unique=True)

    class Meta:
        db_table = 'imports'
