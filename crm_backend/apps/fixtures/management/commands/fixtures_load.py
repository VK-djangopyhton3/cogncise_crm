from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from lead.models import Lead
from core.models import User
from job.models import Job
from customer.models import Customer
from company.models import Company

fake = Faker()

class Command(BaseCommand):
    help = 'Create fake data for (companies, customers, leads and jobs)'

    def add_arguments(self, parser):    
       parser.add_argument('--table', type=str, help='Define which table data to be filled')
       parser.add_argument('--size', type=int, help='Number os records to be created')

    def handle(self, *args, **kwargs):
        for i in range(0, self._get_size(**kwargs)):
            data = { "company_id": ((i % 2 == 0) and 1 or 2) }
            if self._get_table(**kwargs) == 'companies':
                self.create_company(**data)
            if self._get_table(**kwargs) == 'customers':
                self.create_customer(**data)
            if self._get_table(**kwargs) == 'leads':
                data.update({ "owner_id": ((i % 2 == 0) and 2 or 3) })
                self.create_lead(**data)
            if self._get_table(**kwargs) == 'jobs':
                self.create_job(**data)

    # set number of record/s to be created
    def _get_size(self, **kwargs):
        return kwargs.get('size', 0)

    # set which type of record/s to be created
    def _get_table(self, **kwargs):
        return kwargs.get('table', None)

    # initialize user data dict
    def _user_data(self, **kwargs):
        user = {
            "first_name":    fake.first_name(),
            "last_name":     fake.last_name(),
            "email":         fake.unique.ascii_free_email(),
            "username":      fake.user_name(),
            "mobile_number": fake.numerify('+61#########')
        }
        user.update(**kwargs)
        return user

    # initialize address data dict
    def _address_data(self, **kwargs):
        address = {
            "building_number":  fake.building_number(),
            "level_number":     fake.building_number(),
            "unit_type":        fake.building_number(),
            "unit_number":      fake.building_number(),
            "lot_number":       fake.building_number(),
            "street_number":    fake.building_number(),
            "street_name":      fake.street_name(),
            "street_type":      fake.building_number(),
            "suffix":           fake.suffix(),
            "suburb":           fake.state(),
            "state":            fake.state(),
            "pincode":          fake.zipcode()
        }
        address.update(**kwargs)
        return address

    # create a new customer record
    def create_customer(self, **kwargs):
        user_data = { "is_customer": True, "company_id": kwargs.get('company_id', None), "role_type": "customer" }
        user_data = self._user_data(**user_data)
        address_data = self._address_data()

        user = User.objects.create(**user_data)
        customer = Customer.objects.create(user=user, company_id=kwargs.get('company_id', None))
        customer.addresses.create(**address_data)

    # create a new job record
    def create_job(self, **kwargs):
        user_data = {
            "company_id": kwargs.get('company_id', None),
            "title": fake.text(100)
        }
        job_data = self._user_data(**user_data)
        job_data.pop('username')
        property_address = self._address_data()
        property_address.update({ 'purpose': "property" })
        business_address = self._address_data()
        business_address.update({ 'purpose': "business" })

        job = Job.objects.create(**job_data)
        job.addresses.create(**property_address)
        job.addresses.create(**business_address)

    # create a new lead record
    def create_lead(self, **kwargs):
        lead_data = self._user_data()
        lead_data.update({
            "status_id":  randint(1,5),
            "source_id":  randint(1,2),
            "owner_id":   kwargs.get("owner_id", None),
            "company_id": kwargs.get("company_id", None),
        })
        lead_data.pop('username')
        address_data = self._address_data()

        lead = Lead.objects.create(**lead_data)
        lead.addresses.create(**address_data)

    # create a new company record
    def create_company(self, **kwargs):
        email = fake.unique.ascii_free_email()
        owner_data = self._user_data(**{'email': email, 'role_type': 'admin'})
        company_data = {
            "name": fake.company().replace('-', ' ')[:30],
            "abn": fake.bothify(text='###########'),
            "email": email,
            "mobile_number": fake.numerify('+61#########'),
            "status_id": 1
        }
        owner = User.create_company_admin(**owner_data)
        company = Company.objects.create(owner=owner, **company_data)
        owner.company = company
        owner.save()
        company.addresses.create(**self._address_data())
