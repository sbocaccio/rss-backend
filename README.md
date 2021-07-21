# Dependencies:
The project uses pip version 20.3.4 (python 3.9) on Ubuntu. If you need to download python3 go to https://www.python.org/downloads/

*See you pip version running*

    python3 -m pip --version

## Create the virtual environment

**The virtualenv package is required to create virtual environments. You can install it with pip:**

    pip install virtualenv

**To create a virtual environment, you must specify a path. For example to create one in the local directory called ‘mypython’, type the following:**

    virtualenv mypython

**Activate the python environment by running the following command:**

    source mypython/bin/activate

*You should see the name of your virtual environment in brackets on your terminal line e.g. (mypython).
Any python commands you use will now work with your virtual environment*

## Check dependencies
**To check dependencies of the project, run the followings commands inside *backend_site* directory, where you should find a file named __requirements.txt__**

**Install the requirement with:**  

    pip install -r requirements.txt


## Initialize the database
**To initialize the database run in the same directory:**

    python3 ./manage.py migrate


# Useful commands
## How to open the server:

In the same directory run

    python3 ./manage.py runserver

## How to run the tests

    python3 ./manage.py test main_app.tests

## Migrations
When you create or modify a model run inside *backend_site* directory where you should find a file named *manage.py*

    python3 ./manage.py makemigrations
    python3 ./manage.py migrate
    pip freeze > requirements.txt
