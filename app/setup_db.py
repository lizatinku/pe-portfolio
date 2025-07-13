from app.models import TimelinePost
from app.db import mydb

mydb.connect()
mydb.create_tables([TimelinePost])
print("✅ TimelinePost table created!")
