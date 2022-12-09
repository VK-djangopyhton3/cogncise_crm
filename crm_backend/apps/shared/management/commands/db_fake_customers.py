from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from core.models import User
from customer.models import Customer

fake = Faker()

class Command(BaseCommand):
    help = 'Create random customers'

    def add_arguments(self, parser):    
       parser.add_argument('total', type=int, help='Indicates the number of users to be created')


    def handle(self, *args, **kwargs):
        total = kwargs['total']

        for i in range(total):
            user_data = {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.ascii_free_email(),
                "username": fake.user_name(),
                "mobile_number": fake.numerify('9#########'),
                "is_customer": True,
                "company_id": ((i % 2 == 0) and 1 or 2)
            }
            user = User.objects.create(**user_data)

            address_data = {
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
            customer = Customer.objects.create(user=user)
            customer.addresses.create(**address_data)
