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
       parser.add_argument('total', type=int, help='Indicates the number of users to be created')


    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            address_data = {"building_number": fake.building_number(), "level_number": fake.building_number(), "unit_type": fake.building_number(), "unit_number": fake.building_number(), "lot_number": fake.building_number(), "street_number": fake.building_number(), "street_name": fake.street_name(), "street_type": fake.building_number(), "suffix": fake.suffix(), "suburb": fake.state(), "state": fake.state(), "pincode": fake.zipcode()}

            jod_data = {"first_name": fake.first_name(), "last_name": fake.last_name(), "email": fake.email(), "mobile_number": "9698754623", "title": fake.first_name(), "company_id": ((i % 2 == 0) and 1 or 2) }
            job = Job.objects.create(**jod_data)

            address_data.update({'purpose':"property"})
            job.addresses.create(**address_data)

            address_data.update({'purpose':"business"})
            job.addresses.create(**address_data)
