
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
**To check dependencies of the project, run at the root directory:** 

    pip install pipreqs 
    pipreqs 

you can see the dependencies in *requirements.txt*    

**Install them with:**  

    pip install -r requirements.txt

*Advertised: Some modules may be required to install manually since pipreqs sometimes not finds everyone required.*
# Before starting:

## Check migrations
Inside *backend_site* directory you should find a file named *manage.py*

**Check if there are migrations unresolved running**

    python3 ./manage.py makemigrations

**If you have unapplied migrations(s) run**

    python3 ./manage.py migrate

**Now everything has been setup.**

# Useful commands
## How to open the server:

In the same directory run

    python3 ./manage.py runserver

## How to run the tests

    python3 ./manage.py test main_app.tests

