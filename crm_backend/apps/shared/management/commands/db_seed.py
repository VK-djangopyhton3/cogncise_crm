from django.core.management import call_command
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import os

class Command(BaseCommand):
    help = 'Load DB with initial configuration'

    def handle(self, *args, **options):
        try:
            call_command('makemigrations')
            call_command('migrate')
            dir_path = settings.FIXTURE_DIRS[0]
            for ff in os.listdir(dir_path):
                file_path = dir_path + '/' + ff
                call_command('loaddata', file_path)
        except Exception as e:
            raise CommandError(e)

        self.stdout.write(self.style.SUCCESS('Seed completed successfully.'))
