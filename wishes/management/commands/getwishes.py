import asyncio

import genshin
from django.core.management import BaseCommand

from users.models import User
from wishes.models import Wish


class Command(BaseCommand):
    help = 'Get wishes from user'

    @staticmethod
    async def main(url):
        client = genshin.Client(
            game=genshin.Game.GENSHIN,
            lang='ru-ru',
            authkey=genshin.utility.extract_authkey(url),
        )

        wishes = await client.wish_history().flatten()
        await asyncio.sleep(0.5)
        return wishes

    def handle(self, *args, **options):
        url = input('Enter authkey url: ')
        wishes = asyncio.run(self.main(url))

        for item in wishes:
            user = User.objects.get(uid=item.uid)
            wish = Wish(
                id=item.id,
                banner_type=item.banner_type.value,
                name=item.name,
                type=item.type,
                rarity=item.rarity,
                time=item.time,
                user=user,
            )
            wish.save()
            print(f'{("*" * item.rarity):5} {item.type:10} {item.name:30}')
        self.stdout.write(f'Found {len(wishes)} wishes')
