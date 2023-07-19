# Access Control Application

A Microservice Application for managing access and permissions across other microservices that makes up the complete HMS. It helps ensure that only authorized services or users can interact with specific microservices and perform the appropriate actions.

## Tech Stack

**Server:** Python, FastAPI (web framework).

**Database:** MySQL(Production), SQLITE(Test).

**Project Management and Version Control:** BitBucket, Jira, Confluence.

## Installation

To install the project to your local computer or server.

1 Clone into a directory in your computer using:

```bash
git clone git@bitbucket.org:detechnovate/access-control-app.git
```

2 change directory to the project folder created after cloning.
For window users use the command provided below.
For other Operating System Users, Kindly follow online documentation or guide on how to change directory.

```bash
cd <directoryname>
```

3 Creating a virtual environment (this is optional but advisable).

- For window users use the command below. If created successfully, activate the virtual environment.
For other Operating System Users, kindly follow online documentation or guide on how to install and activate your virtual environment.

```bash
virtualenv <virtualenvironmentname>
```

4 Install the required packages, using:

```bash
pip install -r requirements.txt

or

pip3 install -r requirements.txt
```

5 set up the environmment variables. 
## Environment Variable Setup

Follow these steps to set up the necessary environment variables:

- Create a new file named `.env` in the root directory of the project.
- Open the `.env` file in a text editor.
- Add the following variables and their corresponding values:

   ```plaintext
   DB_ACCESS_HOST="server host name e.g localhost"
   DB_ACCESS_USER="username e.g root"
   DB_ACCESS_PASSWORD="enter your password"
   DB_ACCESS_NAME="access_control_app"
   TESTING=please leave this blank as it is required for testing.
   ACCESS_PORT=port_number
   RELOAD=True
   HOST="application ip address e.g 127.0.0.1"
   ACCESS_SECRET_KEY="anystring e.g an alphanumeric character combination advised"
   REFRESH_SECRET_KEY="anystring e.g an alphanumeric character combination advised"
   ```

- Save it.

6 Ensure you have your database server start up. 

7 Create the database with name 'access_control_app'. you can do this manually or which ever way is convenient for you.

8 Run migrations to prepare the models or table to be added to the database, using:

```bash
alembic revision --autogenerate -m "migration name"
```

9 Migrate your tables to the database, using:

```bash
alembic upgrade head
```

10 Finally, you can run your server using:
```bash
python main.py

or

python3 main.py

or 

pytest (for testing)
```

## Features

NOTE: A majority of features provided by the API requires an Authorization header and or a bearer token. All endpoints requires an Authorization header except;
```bash
PATCH /client/reactivate/client_id
POST /client/create
GET /client/
```

The Authorization header should be included in the request as follows:
```bash
Client-Authorization: client_key_value
```

The bearer token (access token) is generated once you are successfully logged in.

The bearer token should be added on the Auth bearer part of your api test service while testing.

## License
Project idea was inspired by [INTUITIVE]
