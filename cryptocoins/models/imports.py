from peewee import Model, PostgresqlDatabase, DateTimeField, TextField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Imports(BaseModel):
    created_at = DateTimeField()
    date_dir = TextField(null=True)
    file_name = TextField(null=True, unique=True)
    remote_dir = TextField(null=True)

    class Meta:
        db_table = 'imports'
