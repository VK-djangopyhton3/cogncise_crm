# Cogncise CRM Backend

## Clone the project

```bash
# navigate to project root directory: `/var/www` Or any other path
git clone git@github.com:repository/name.git cogncise
```

## Create Environment file

```bash
# navigate inside project directory
cd cogncise

# create a new environment file
cp example.ini crm_backend/settings/settings.ini
```

- Note : Replace the variable values as per your system or machine.

## Setup Virtual Environment

```bash
# create a new virtual environment by
virtualenv --python=python3.10 .venv
```

### Setup Backend Code

```bash
# activate virtualenv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# build migrations
python3 manage.py makemigrations

# apply or migrate migrations
python3 manage.py migrate
```

## Setup First User

```bash
# create a new superuser and fill the details as per prompted command
python3 manage.py createsuperuser
```

## Dump & Load base data

Dump Fixtures:

```bash
./manage.py dumpdata core.group > crm_backend/fixtures/core/group.json
```

Load complete dataset

```bash
# load default complete dataset
python3 manage.py fixtures_load_dump
```

Load fixtures:

```bash
# groups/roles
python3 manage.py loaddata crm_backend/fixtures/core/groups.json

# users
python3 manage.py loaddata crm_backend/fixtures/core/users.json

# companies
python3 manage.py loaddata crm_backend/fixtures/company/companies.json

# lead statuses
python3 manage.py loaddata crm_backend/fixtures/lead/leadstatus.json

# lead sources
python3 manage.py loaddata crm_backend/fixtures/lead/leadsource.json
```

## Create/Load dummy data

- `--table` &nbsp;&nbsp;
  argument accepts from following customers, leads and jobs
- `--size` &nbsp;&nbsp;&nbsp;&nbsp;
  argument accepts integer value for number of records to create

```bash
# create or load companies data
./manage.py fixtures_load --table=companies --size=10

# create or load customers data
./manage.py fixtures_load --table=customers --size=100

# create or load leads data
./manage.py fixtures_load --table=leads --size=100

# create or load jobs data
./manage.py fixtures_load --table=jobs --size=100
```
