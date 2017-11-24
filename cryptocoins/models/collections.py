from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Collections(BaseModel):
    created_at = DateTimeField()
    name = TextField(index=True)
    url = TextField()

    class Meta:
        db_table = 'collections'
        indexes = (
            (('created_at', 'name'), True),
        )

    @classmethod
    def create_collection(cls, name, url):
        try:
            with database.atomic():
                return cls.create(name=name, url=url)
        except IntegretyError:
            print(f"ERROR COLLECTION EXISTS: {name}, {url}")
            return None
