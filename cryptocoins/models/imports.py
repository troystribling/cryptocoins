from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BooleanField
import logging
from dateutil.parser import parse

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
            logger.warn(f"DATABASE ERROR FOR Imports: {error}: {path}/{date_dir}/{file_name}")
            return None

    @classmethod
    def find_for_file_name(cls, file_name):
        return cls.raw("SELECT * FROM imports WHERE file_name=%s", file_name)

    @classmethod
    def last_import_date_for_path(cls, path):
        query = cls.raw("SELECT date_dir, MAX(created_at) AS created_at, path"
                        " FROM imports"
                        "  GROUP BY date_dir, path, success"
                        "   HAVING path=%s"
                        "    AND success=TRUE"
                        " ORDER BY created_at DESC LIMIT 1", path)
        last_import = [last_import for last_import in query]
        if len(last_import) < 1:
            return None
        return parse(last_import[0].date_dir)
        
    def import_successful(self):
        query = Imports.update(success=True).where((Imports.id == self.id))
        query.execute()
