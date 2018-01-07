from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BooleanField
import logging


logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', user='cryptocoins', host='127.0.0.1')


class BaseModel(Model):
    class Meta:
        database = database


class Collections(BaseModel):
    created_at = DateTimeField()
    path = TextField(index=True)
    success = BooleanField()
    url = TextField()
    meta = TextField()

    class Meta:
        db_table = 'collections'
        indexes = (
            (('created_at', 'path'), True),
        )

    @classmethod
    def create_collection(cls, path, url, meta):
        try:
            with database.atomic():
                return cls.create(path=path, url=url, meta=meta)
        except IntegrityError as error:
            logger.error(f"DATABASE ERROR FOR Collection: {error}: {path}, {created_at}")
            return None

    @classmethod
    def get_for_id(cls, id):
        try:
            return cls.get(Collections.id == id)
        except IntegrityError as error:
            logger.error(f"DATABASE ERROR FOR Collection with id: {error}: {id}")
            return None

    @classmethod
    def lastest_collection_for_url(cls, url):
        query = "SELECT created_at FROM collections WHERE url = %s AND success = 'true' ORDER BY created_at LIMIT 1"
        return cls.raw(query, url).scalar()

    @classmethod
    def lastest_collection_for_path_and_meta(cls, url, meta):
        query = "SELECT created_at FROM collections WHERE path = %s AND meta = %s AND success = 'true' ORDER BY created_at LIMIT 1"
        return cls.raw(query, url, meta).scalar()

    def collection_successful(self):
        query = Collections.update(success=True).where((Collections.id == self.id))
        query.execute()
