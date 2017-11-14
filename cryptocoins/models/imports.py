from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, IntegrityError

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

    @classmethod
    def create_import(cls, date_dir, file_name, remote_dir):
        try:
            with database.atomic():
                return cls.create(date_dir=date_dir, file_name=file_name, remote_dir=remote_dir)
        except IntegrityError:
            print(f"ERROR IMPORT EXISTS: {remote_dir}/{date_dir}/{file_name}")
            return None
