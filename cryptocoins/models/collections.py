from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BooleanField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


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

    @classmethod
    def get_with_id(cls, id):
        try:
            return Collections.get(Collections.id == id)
        except IntegrityError as error:
            print(f"ERROR: Collection with id {id} exists: : {error}")
            return None

    @classmethod
    def last_successful_collection_for_url(cls, url):
        query = "SELECT created_at, path, url, success FROM collections" \
                " WHERE url = %s AND success = 'true'" \
                " ORDER BY created_at LIMIT 1"
        return cls.raw(query, url).scalar()

    def collection_successful(self):
        query = Collections.update(success=True).where((Collections.created_at == self.created_at) & (Collections.path == self.path))
        query.execute()

    def lastest_collection_for(url):
        query = "SELECT created_at FROM collections WHERE url = %s AND success = 'true' ORDER BY created_at LIMIT 1"
        return Collections.raw(query, url).scalar()
