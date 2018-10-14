This are the files for Udaan Developer Hiring Challenge on hackerearth. This application is made using flask framework in python language. It uses mysql database and sqlalchemy as an sql ORM tool. I used postman tool to test the API and have provided screenshots for each request in case this appliction does not run on your system.

tl;dr;
Language: Python
Database: Mysql
ORM: SqlAlchemy

IMPORTANT INSTRUCTIONS:
    - Due to lack of time I was not able to create a proper DBMS configuration file. I created a temporary config file to provide MySQL configurations
    - Edit the ./dbSetup/db.config file and paste the configuration in this specific order:
        UdaanDB,<user>,<password>
    - Create the UdaanDB database in your mysql database to avoid errors while execution.
    - Run the following commmand to install all requirements and then run the application:
        pipenv --python=2
        pipenv install
        pipenv shell
        python app.py
    - After completing the above commands, you would have successfully ran the application on localhost:9090.
    - Use the below mentioned documentation as a guide to uses the API.

API Documentation: https://documenter.getpostman.com/view/3383671/RWgrxxKV