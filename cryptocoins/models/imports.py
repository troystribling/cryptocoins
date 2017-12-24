from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Imports(BaseModel):
    created_at = DateTimeField()
    date_dir = TextField()
    file_name = TextField(unique=True)
    remote_dir = TextField()

    class Meta:
        db_table = 'imports'

    @classmethod
    def create_import(cls, date_dir, file_name, remote_dir):
        try:
            with database.atomic():
                return cls.create(date_dir=date_dir, file_name=file_name, remote_dir=remote_dir)
        except IntegrityError as error:
            print(f"DATABASE ERROR for Imports: {error}: {remote_dir}/{date_dir}/{file_name}")
            return None
