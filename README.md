# Udacity Item Catalog Project

Overview
--------
This is the git repository for Project 5.  It is an item catalog of books and book categories.  Installation instructions are below.

Installation
------------

###### Setting up the database and environment
1. Download the files from the git repository into one directory
2. If you do not have Vagrant and VirtualBox installed, then please follow the instructions [here](https://www.udacity.com/wiki/ud088/vagrant "Vagrant Installation Instructions")
3. In your command line, navigate to the directory where you've installed your files and type the following:
```shell
$ vagrant up  # this will take some time, then run the second line below
$ vagrant ssh  # this will open up the virtual machine command line
```
4. Navigate to the shared vagrant directory with the following command: `cd /vagrant`
5. Create the database and populate it with an initial set of books like so:
```shell
$ python database_setup.py  # books.db will be set up
$ python lotsofbooks.py  # this will populate an initial set of books and book categories.  If successful, the book titles and categories will be printed
```
###### Create client_secrets.json file
1. Go to Google's [API Console](https://console.developers.google.com/projectselector/apis/library, "API Console").
2. Click "Create New Project"
3. Type in a project name.
4. In the sidebar under "API Manager", select Credentials, then select the OAuth consent screen tab.
5. Specify a project name.
6. Under Application type, select Web application.
7. In the Authorized JavaScript origins field, enter the origin for your app. In this case, we are using the following: `http://localhost:5000`
8. Then, in the Authorized redirect URIs add the following two URLs:
```
http://localhost:5000
http://localhost:5000/login
```
9. Click on "Save".
10. Then click on "Download JSON" at the top of the screen.
11. Navigate to your Downloads folder and rename this file to `client_secrets.json`.
12. Move the file `client_secrets.json` to the directory where you downloaded the git project.

###### Running the project
1. If you have logged out of vagrant, go back to your project directory and type the following:
```shell
$ vagrant up  # this will take some time, then run the second line below
$ vagrant ssh  # this will open up the virtual machine command line
```
2. Navigate to the shared vagrant directory with the following command: `cd /vagrant`.
3. Type `python project.py` on the command line.  This should fire up the server.
4. Go to the browser and navigate to `http://localhost:5000/`