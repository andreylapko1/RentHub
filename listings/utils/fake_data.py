import os
import random

from cities_light.models import City
from users.models import User
from faker import Faker

from listings.models import Listing
from rentapp import settings

fake = Faker()

def choise_random_img():
    folder = os.path.join(settings.MEDIA_ROOT, 'listings', 'images')
    if not os.path.exists(folder):
        raise FileNotFoundError(f'Folder does not exist: {folder}')
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        raise FileNotFoundError(f'No image files found in {folder}')
    filename = random.choice(files)
    return os.path.join('listings', 'images', filename)


def create_ads(user):
    title = fake.sentence(nb_words=5)
    description = fake.text(max_nb_chars=300)
    rooms = random.randint(1, 4)
    price = random.randint(90, 50)
    type = random.choice(['home', 'appartment'])
    qs = City.objects.filter(country__name='Germany')
    count = qs.count()
    location = qs[random.randint(0, count - 1)]

    listing = Listing.objects.create(
        title=title,
        description=description,
        location=location,
        price=price,
        rooms=rooms,
        type=type,
        image=choise_random_img(),
        created_at=fake.date_this_decade()
    )
    return listing


def filling_db(n=100):
    users = User.objects.all()
    for _ in range(n):
        user = random.choice(users)
        create_ads(user)
        print(f'Объявление для пользователя {user.username}')