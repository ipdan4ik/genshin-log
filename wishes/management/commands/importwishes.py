import asyncio
import datetime
import json

import genshin as genshin
import pytz
from django.core.management import BaseCommand

from users.models import User
from wishes.models import Wish


class Command(BaseCommand):
    help = 'Import wishes from json'

    def handle(self, *args, **options):
        wishes = json.load(open('wishes_wish.json', 'rb'))

        for item in wishes:

            if item['id'] >= 1648789560000828134:
                continue

            user = User.objects.get(uid=item['uid'])

            dt = datetime.datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S')
            tz = pytz.timezone('Africa/Lagos')
            dt = tz.localize(dt)

            wish = Wish(
                id=item['id'],
                banner_type=item['banner_type'],
                name=item['name'],
                type=item['type'],
                rarity=item['rarity'],
                time=dt,
                user=user,
            )
            wish.save()
        self.stdout.write(f'Found {len(wishes)} wishes')
