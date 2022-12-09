from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from lead.models import Lead

fake = Faker()

class Command(BaseCommand):
    help = 'Create random leads'

    def add_arguments(self, parser):    
       parser.add_argument('total', type=int, help='Indicates the number of users to be created')


    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            lead_data = { "first_name": fake.first_name(), "last_name": fake.last_name(), "email": fake.email(), "mobile_number": "9698754623", "status_id": randint(1,5), "source_id": randint(1,2), "owner_id": ((i % 2 == 0) and 2 or 3), "company_id": ((i % 2 == 0) and 1 or 2) }
            lead = Lead.objects.create(**lead_data)

            address_data = {"building_number": fake.building_number(), "level_number": fake.building_number(), "unit_type": fake.building_number(), "unit_number": fake.building_number(), "lot_number": fake.building_number(), "street_number": fake.building_number(), "street_name": fake.street_name(), "street_type": fake.building_number(), "suffix": fake.suffix(), "suburb": fake.state(), "state": fake.state(), "pincode": fake.zipcode()}
            lead.addresses.create(**address_data)
