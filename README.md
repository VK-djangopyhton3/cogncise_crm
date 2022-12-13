# Cogncise CRM Backend

## Clone the project

### Clone the project from Github:

    Project Root Directory: `/var/www` Or any

    git clone remote url

## Create Environment file

    Go to the settings folder then create settings.ini or .env file

    Note : Like see the example.ini file in project root folder, same veriable copy and paste in settings.ini file on settings folder then update env varible .

## Virtual Environment Setup

### Create Virtualenv Folder

    virtualenv --python=python3.10 Project_dir/.venv

### Backend python code

### Activate Environment:

    source project_venv/bin/activate

## Install dependencies:

    pip install -r requirements.txt

## Apply database migrations

    python3 manage.py makemigrations
    python3 manage.py migrate

## Create super user

    python3 manage.py createsuperuser

## Load & Dump base data

Dump Fixtures:

    ./manage.py dumpdata core.group > crm_backend/fixtures/core/group.json

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

- `--table` argument accepts from following customers, leads and jobs
- `--size` argument accepts integer value for number of records to create

```bash
# create or load customers data
./manage.py db_seed_fake --table=customers --size=10

# create or load leads data
./manage.py db_seed_fake --table=leads --size=10

# create or load jobs data
./manage.py db_seed_fake --table=jobs --size=10
```
