import faker


def get_payload_user() -> dict:
    fake = faker.Faker()
    payload = {
        "email": fake.email(),
        "password": fake.password(7),
        "name": fake.name()

    }
    return payload

