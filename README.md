# Description

##Proces of the project
### Data Loading
1. The files are loaded according to their size. The largest file is kept at the end of the list.
2. According to the file names, different wrapper classes are called which validate the file and save the data to their table. To load files with other data, please keep the names
the same as the ones in the resource folder.
3. Person is the largest file as it has person related to company and food and with other people as friends.
4. Fruits and vegetables json files were not given in the email so I went ahead and made my own.
5. So, company, fruits and vegetables are checked (validation) and saved first. Then person is loaded and their relations are saved.
6. Rows that aren't valid are skipped.

# Requirements
1. Pycharm (VScode can be used too, but the virtualenv setup can be different)
2. Django
3. Django restframework
4. mysql
5. mysql client
6. mysql workbench
# Setup Instructions
1. First run the setup database
2. Install the requirements
3. Load the data
## Setup database
1. Make sure mysql client is installed. If not run: ``arch -x86_64 brew install mysql``. this is for macbook m1.
This is needed for mysqlclient to work with mysql database.
2. Create a new user in mysql to use with this project and grant privileges: 

`CREATE USER '<user_name>'@'localhost' IDENTIFIED BY 'password';`

Need to grant privileges to the user:

`GRANT ALL PRIVILEGES ON `mytestdb`.* TO `<user_name>`@`%`

To grant privileges to the user to create test database which will be used to 
run the test files.
3. Replace the username and password in the settings.py file

`GRANT ALL PRIVILEGES ON `test_mytestdb`.* TO `ridwan`@`%`

##Install requirements
1. Install virtualenv by running `virtualenv venv`
2. activate virtualenv (source venv/bin/activate)
3. run `pip install -r requirements.txt`
4. Migrate the database by running `python manage.py migrate`
5. You can create a superuser too by running `python manage.py createsuperuser`

## Load data
1. It was assumed that the file names that will be used with this project are
`companies.json` and `people.json`. If new files are used, please keep the
file names constant to `companies.json` and `people.json` as the names were used
to keep the logic of different schemas constant
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
4. Recommeded way to access the APIs is through postman

##Accessing the APIs
1. First question was

`Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.`

Open postman and go to url `http://localhost:8000/q1/<index_number>`. 
The `index_number` is the number for the company.
2. Second question was

`Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.`

Replace the `person_index` in the below API with the index from people and run it
`http://localhost:8000/q2?person<person_index>=&person2=<person_index>`

3. Third question was: 

`Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

Replace the `http://localhost:8000/q3/<person_index>` with the index of the person.


# Running the tests
There are two test files available. To run them, please run
1. python manage.py test data_loader - This will run the test available in data_loader
2. python manage.py test api - This tests the 3 questions that was in the email