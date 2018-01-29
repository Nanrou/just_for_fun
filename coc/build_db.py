import json

from peewee import *

db = SqliteDatabase('db.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Skill(BaseModel):
    name = CharField(max_length=32)
    default_point = SmallIntegerField()
    modern = BooleanField()
    normal = BooleanField()
    description = TextField()
    auxiliary_text = TextField()


if __name__ == '__main__':
    pass

