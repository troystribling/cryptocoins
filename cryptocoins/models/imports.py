from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BooleanField
import logging


logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', user='cryptocoins', host='127.0.0.1')


class BaseModel(Model):
    class Meta:
        database = database


class Imports(BaseModel):
    created_at = DateTimeField()
    date_dir = TextField()
    file_name = TextField(unique=True)
    path = TextField()
    success = BooleanField()

    class Meta:
        db_table = 'imports'

    @classmethod
    def create_import(cls, date_dir, file_name, path):
        try:
            with database.atomic():
                return cls.create(date_dir=date_dir, file_name=file_name, path=path)
        except IntegrityError as error:
            logger.warn(f"DATABASE ERROR FOR Imports: {error}: {remote_dir}/{date_dir}/{file_name}")
            return None

    def import_successful(self):
        query = Imports.update(success=True).where((Imports.id == self.id))
        query.execute()
