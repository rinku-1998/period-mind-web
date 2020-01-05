# Period Mind Website
A webAPI for a iOS App in final project

## Environment
* Windows **(CANNOT be used in production deployment)**
* Linux based system (eg.Ubuntu)
* OS X

## Prerequisites
* [Python](https://www.python.org/downloads/) >=3.6
* Pipenv

## Installation
```
git clone https://github.com/www563214789/ios_finalProject_web.git
cd ios_finalProject_web
pipenv install
``` 

## First Use
```
flask db upgrade  #Build SQL structure for first use
```

## For Production deployment
1.You have to build your own `.env` file in producion deployment
```
# Create .env
touch .env
```
2.You have to set enviroment variables in `.env` file
```
SECRET_KEY = [YOUR SECRECT_KEY HERE] #You can use UUID generator to create one
#If you need to use MySQL server instead of SQLite
DATABASE_URL = mysql+pymysql://[SQL_USERNAME]:[SQL:PASSWORD]@[SQL_SERVER_URL]:[SQL_SERVER_PORT]/[SQL_DATABASE_NAME] 
```

## Run
```
# For development 
flask run
# For production deployment
gunicorn -b localhost:port -w NUM_WORKER wsgi:app 
```