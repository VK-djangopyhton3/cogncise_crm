from django.core.management import call_command
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import os, time

class Command(BaseCommand):
    help = 'Load DB with initial configuration'

    def handle(self, *args, **options):
        try:
            print('=====> makeing migrations <=====')
            call_command('makemigrations')

            print('=====> migrating database <=====')
            call_command('migrate')

            print('=====> fetching fixture files <=====')
            dir_path = settings.FIXTURE_DIRS[0]
            files = os.listdir(dir_path)
            time.sleep(3)
            files.sort()

            print('=====> running fixtures <=====')
            for ff in files:
                file_path = dir_path + '/' + ff
                print('=====> ', ff, ' <=====')
                call_command('loaddata', file_path)
        except Exception as e:
            raise CommandError(e)

        self.stdout.write(self.style.SUCCESS('Seed completed successfully.'))
