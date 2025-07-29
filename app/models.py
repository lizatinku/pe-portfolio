from peewee import Model, CharField, TextField, DateTimeField
from datetime import datetime
from . import mydb 

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

timeline_post = TimelinePost
