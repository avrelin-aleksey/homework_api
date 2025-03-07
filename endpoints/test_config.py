from faker import Faker


fake = Faker()

memes_data = {
    "text": fake.sentence(),
    "url": fake.image_url(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
memes_data_post_id = {
    "id": 22,
    "text": fake.sentence(),
    "url": fake.image_url(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
memes_data_negative1 = {
    "text": fake.sentence(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
memes_data_negative2 = {
    "url": fake.image_url(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
memes_data_negative3 = {
    "info": {"key": fake.uuid4()},
}
memes_data_negative4 = {
    "tags": [fake.word() for _ in range(3)],
}
memes_data_negative5 = {
    "id": 22,
    "text": fake.sentence(),
    "url": fake.image_url(),
}
empty_value = {
    "text": "",
    "url": "",
    "tags": [],
    "info": {}
}
long_text = {
    "text": "ЫЫВы" * 1000,
    "url": fake.image_url(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
invalid_tags = {
    "text": fake.sentence(),
    "url": fake.image_url(),
    "tags": "не валидный",
    "info": {"key": fake.uuid4()},
}
