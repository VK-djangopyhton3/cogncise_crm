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
    
    ./manage.py dumpdata core.role > crm_backend/fixtures/core/role.json

Load fixtures:

    #python3 manage.py loaddata crm_backend/fixtures/core/group.json
    python3 manage.py loaddata crm_backend/fixtures/offer_manager/role.json