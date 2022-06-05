# Description

# Project Structure
```
├── app
    └── endpoints
        └── __init__.py
        └── feature_endpoints.py
        └── viewsets
    └── __init__.py
    └── apps.py
    └── exceptions.py
    └── serializers.py
    └── services.py
    └── tests.py
    └── urls.py

├── data_loader
    └── management
        └── commands
            └── ...
            └── load_data.py
    └── migrations
    └── wrappers
        └── ...
        └── Company.py
        └── Fruit.py
        └── People.py
        └── Vegetable.py
        └── Wrapper.py
    └── ...
    └── models.py
    └── tests.py

├── resource
    └── companies.json
    └── people.json
    └── fruits.json
    └── vegetables.json

├── stockspot
    └── ...
    └── settings.py
└── README.md
```
stockspot -> Main project folder with the settings file

data_loader -> Takes care of data loading and validation

api -> urls route to services which is routed to endpoints/feature_endpoints.py (contains the business logic)

## Process of the project
### Data Loading
1. The files are loaded according to their size. Main logic is inside `data_loader/management/commands/load_data.py`. 
JSON files should be kept in the `resource` folder. `load_data` loads the largest file last.
2. According to the file names, different wrapper classes are called which validate the file and save the data to their table. To load files with other data, please keep the names
the same as the ones in the resource folder.
3. Person is the largest file as it has person related to company and food and with other people as friends.
4. Fruits and vegetables json files were not given in the email so I went ahead and made my own.
5. So, company, fruits and vegetables are checked (validation) and saved first. Then person is loaded and their relations are saved.
6. Rows that aren't valid are skipped.

### Accessing the APIs (after data loading)
1. Run the server using `python manage.py runserver`.
2. Go to `localhost:8000` to access the apis to view the data. Can only access companies, people, fruits, vegetables.
3. To access the API features asked, please use postman to access. Instructions are provided
in this readme.

# Requirements
1. Pycharm (VScode can be used too, but the virtualenv setup can be different)
2. Django
3. Django restframework
4. mysql
5. mysql client
6. (Optional) mysql workbench (gui to view data)

# Setup Instructions
1. First run the setup database
2. Install the django requirements
3. Load the data
4. Access the APIs

## Setup database
1. Make sure mysql client is installed. If not run: ``arch -x86_64 brew install mysql``. this is for macbook m1.
This is needed for mysqlclient to work with mysql database (in virtualenv). Otherwise might
throw an error as pip install command installs mysqlclient that is used by the python project.
2. Create a new user in mysql to use with this project and grant privileges: 

`CREATE USER '<user_name>'@'localhost' IDENTIFIED BY 'password';`

To check if user has been created, please run:

`select user from mysql.user;`

Create a new database:

`CREATE DATABASE db_name;`

Need to grant privileges to the user for the database:

`GRANT ALL PRIVILEGES ON db_name. * TO '<user_name>'@'localhost';`

To grant privileges to the user to create test database which will be used to 
run the test files. Replace the username and password in the settings.py file. There are multiple
tests that depend on the test database so this command should be run:

`GRANT ALL PRIVILEGES ON test_db_name. * TO '<user_name>'@'localhost';`

3. Replace the database name, user and password in the stockspot.settings Database configuration.

The process for postgres should be more or similar. Also need to change the database
config to postgres in settings.

## Install requirements
1. Install virtualenv by running `virtualenv venv`
2. activate virtualenv (source venv/bin/activate)
* While developing, conda env was used with pycharm
3. run `pip install -r requirements.txt`
4. Migrate the database by running `python manage.py migrate`
5. (Optional) You can create a superuser too by running `python manage.py createsuperuser`

## Load data
1. It was assumed that the file names that will be used with this project are
`companies.json` and `people.json`. If new files are used, please keep the
file names constant to `companies.json` and `people.json` as the names were used
to keep the logic of different schemas constant. Please view the Wrapper class in data_loader app.
2. `fruits.json` and `vegetables.json` were not present in the email so I am not sure 
about their schema. I assumed a schema for fruits and vegetables and included in the resource file
3. To load the data run `python manage.py load_data`
4. Files are loaded according to their size. The people.json file is the biggest
with the most data, so companies, fruits and vegetables are loaded first.

## Running the project
1. The project should run now
2. Run `python manage.py runserver' to keep the server running
3. Go to url `localhost:8000`. It will show some available apis. The data that was input
can be viewed there.
4. Recommended way to access the APIs is through postman
5. To get the correct error messages, please change `debug=False` in settings. However
this might load the browserable API (`localhost:8000`) without templates

## Accessing the APIs
1. First question was

`Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.`

Open postman and go to url `http://localhost:8000/all_company_employees/<company_index>`.

<company_index> should be integer.

2. Second question was

`Given 2 people, provide their information (Name, Age, Address, phone) and the list of 
their friends in common which have brown eyes and are still alive.`

Replace the `person_index` in int format in the below API with the index of people from people.json and run it

`http://localhost:8000/common_people?person1=<person1_index>&person2=<person2_index>`

3. Third question was:
\
Given 1 people, provide a list of fruits and vegetables they like. 
This endpoint must respect this interface for the output: 

`{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

Replace the `http://localhost:8000/person_liked_fruits_veges/<person_index>` 

with the int index of the person from people.json.


# Running the tests
There are two test files available. To run them, please run
1. `python manage.py test data_loader` - This will run the test available in data_loader
2. `python manage.py test api` - This tests the 3 questions that was in the email

# Assumptions
1. the index field could not be used as primary key as it starts from 0 and
sql creates records from 1.
2. Fruits and vegetables json file was not provided so I went ahead and made my own
3. Question 2 was not clear, if 2 person was given and one of them has brown eyes 
and is alive, does that mean that person is a common friend? I assumed they are not so
that person is excluded in the api
4. To make the project more modular, wrappers were used which were called by the name
of the file. The main idea was to support more formats of json files. Each new format 
of file would be added to the wrapper with the file name.
