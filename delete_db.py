import os

db_path = 'instance/iara.db'

if os.path.exists(db_path):
    os.remove(db_path)
    print("Yes!")
else:
    print("No")