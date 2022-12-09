from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from lead.models import Lead
from core.models import User
from job.models import Job
from shared.models import Address

fake = Faker()

class Command(BaseCommand):
    help = 'Create random jobs'

    def add_arguments(self, parser):    
       parser.add_argument('--table', type=str, help='Define which table data to be filled')
       parser.add_argument('--size', type=int, help='Number os records to be created')


    def handle(self, *args, **kwargs):
        for i in range(1, self.size()):
            if self.table() == 'customers':
                self.customer()
            if self.table() == 'leads':
                self.lead()
            if self.table() == 'jobs':
                self.job()


    def customer(self, **kwargs):
        pass

    def job(self, **kwargs):
        pass
    
    def lead(self, **kwargs):
        pass


    def size(self, **kwargs):
        return kwargs.get('size', 0)
    
    def table(self, **kwargs):
        return kwargs.get('table', None)


    def address(self, **kwargs):
        address = {
            "building_number": fake.building_number(),
            "level_number": fake.building_number(),
            "unit_type": fake.building_number(),
            "unit_number": fake.building_number(),
            "lot_number": fake.building_number(),
            "street_number": fake.building_number(),
            "street_name": fake.street_name(),
            "street_type": fake.building_number(),
            "suffix": fake.suffix(),
            "suburb": fake.state(),
            "state": fake.state(),
            "pincode": fake.zipcode()
        }
        return address.update(**kwargs)

    def user(self, **kwargs):
        user = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.ascii_free_email(),
            "username": fake.user_name(),
            "mobile_number": fake.numerify('9#########')
        }
        return user.update(**kwargs)
