from faker import Faker
from lead.models import Lead
from core.models import User
from job.models import Job
from shared.models import Address

fake = Faker()


def create_lead_data(x):

    user_data = {"first_name": fake.first_name(), "last_name": fake.last_name(), "email": fake.email(), "mobile_number": "9698754623", "username" : fake.user_name()}

    user = User.objects.create(**user_data)

    lead_data = { "first_name": fake.first_name(), "last_name": fake.last_name(), "email": fake.email(), "mobile_number": "9698754623", "status_id": x, "source_id": 1, "owner": user}

    lead = Lead.objects.create(**lead_data)

    address_data = {"building_number": fake.building_number(), "level_number": fake.building_number(), "unit_type": fake.building_number(), "unit_number": fake.building_number(), "lot_number": fake.building_number(), "street_number": fake.building_number(), "street_name": fake.street_name(), "street_type": fake.building_number(), "suffix": fake.suffix(), "suburb": fake.state(), "state": fake.state(), "pincode": fake.zipcode()}

    lead.addresses.create(**address_data)

for x in range(5):
    num = 5
    for x in range(num):

        create_lead_data(x+1)


def create_job_data():
    address_data = {"building_number": fake.building_number(), "level_number": fake.building_number(), "unit_type": fake.building_number(), "unit_number": fake.building_number(), "lot_number": fake.building_number(), "street_number": fake.building_number(), "street_name": fake.street_name(), "street_type": fake.building_number(), "suffix": fake.suffix(), "suburb": fake.state(), "state": fake.state(), "pincode": fake.zipcode()}

    jod_data = {"first_name": fake.first_name(), "last_name": fake.last_name(), "email": fake.email(), "mobile_number": "9698754623", "title": fake.first_name() }

    job = Job.objects.create(**jod_data)

    address_data.update({'purpose':"property"})
    job.addresses.create(**address_data)

    address_data.update({'purpose':"business"})
    job.addresses.create(**address_data)

for x in range(10):
    create_job_data()