import asyncio

import genshin as genshin
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Get users from browser cookies'

    @staticmethod
    async def main():
        client = genshin.Client(game=genshin.Game.GENSHIN)
        client.set_browser_cookies()
        accounts = await client.get_game_accounts()
        await asyncio.sleep(0.5)
        users = list(accounts)
        return users

    def handle(self, *args, **options):
        accounts = asyncio.run(self.main())
        for account in accounts:
            user = User(
                uid=account.uid,
                nickname=account.nickname,
                server=account.server
            )
            user.save()
        self.stdout.write(f'Found {len(accounts)} accounts')
