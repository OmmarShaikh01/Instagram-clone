import json
import random
import uuid

from passlib.hash import django_pbkdf2_sha256

# creates user app data
password = django_pbkdf2_sha256.using(rounds=390000, salt_size=16).hash("qwerty123456")
user_pks = [str(uuid.uuid4()) for pk in range(100)]
data = [
    {
        "model": "user.usermodel",
        "pk": pk,
        "fields": {
            "password": password,
            "user_name": f"admin_{i + 1}",
            "user_phone": random.randint(1000000000, 9999999999),
            "user_email": f"admin_{i + 1}@testmail.com",
            "user_account_createdOn": "2023-01-03",
        },
    }
    for i, pk in enumerate(user_pks)
]

with open("tests/user/load_data.json", "w") as fp:
    fp.write(json.dumps(data, indent=4))

# creates user_relationship app data
from_users = user_pks[0:10]
to_users = user_pks[0 + 10: 10 + 10]
data = []
for f, t in zip(from_users, to_users):
    data.append(
        {
            "model": "user_relationship.userrelationshipmodel",
            "pk": str(uuid.uuid4()),
            "fields": {"relationship_user_uuid": f, "relationship_friend_uuid": t, "relationship_status": "FRD"},
        }
    )
    data.append(
        {
            "model": "user_relationship.userrelationshipmodel",
            "pk": str(uuid.uuid4()),
            "fields": {"relationship_user_uuid": t, "relationship_friend_uuid": f, "relationship_status": "FRD"},
        }
    )

to_users = user_pks[0 + 20: 10 + 20]
for f, t in zip(from_users, to_users):
    data.append(
        {
            "model": "user_relationship.userrelationshipmodel",
            "pk": str(uuid.uuid4()),
            "fields": {"relationship_user_uuid": t, "relationship_friend_uuid": f, "relationship_status": "FRD"},
        }
    )

to_users = user_pks[0 + 30: 10 + 30]
for f, t in zip(from_users, to_users):
    data.append(
        {
            "model": "user_relationship.userrelationshipmodel",
            "pk": str(uuid.uuid4()),
            "fields": {"relationship_user_uuid": t, "relationship_friend_uuid": f, "relationship_status": "BLK"},
        }
    )

to_users = user_pks[0 + 40: 10 + 40]
for f, t in zip(from_users, to_users):
    data.append(
        {
            "model": "user_relationship.userrelationshipmodel",
            "pk": str(uuid.uuid4()),
            "fields": {"relationship_user_uuid": t, "relationship_friend_uuid": f, "relationship_status": "PND"},
        }
    )

with open("tests/user_relationship/load_data.json", "w") as fp:
    fp.write(json.dumps(data, indent=4))
