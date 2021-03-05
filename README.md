# Forleti - Backend
The Forleti project is an implementation of a settings menu for a rapidly growing social media application. This project was built with focuses on ease of development and collaboration.  Forleti utilizes a modular programming style, clear annotations, and expressive tests.

This repository is the REST API backend for the blogging app, written with Flask and PostgreSQL. It features a modular design, with an Application Factory Pattern, Blueprints, and testing fixtures. The goal is to eventually utilize a microservices architecture. 

Check out the Frontend Repository [here!](https://github.com/nbry/forleti-fe "here!")

## Developer Features:

- **Application Factory Pattern**

	A function `create_app()` initializes a Flask application, links blueprints, and adds extensions. Because of the factory pattern, multiple apps can be run in parallel. This will be crucial for setting up a microservices architecture.

- **Testing Fixtures**

	Using the application factory pattern, I set up a testing fixture for testing routes and functions within the Forleti backend. Tests are conducted with Pytest.

- **Configurable Environment Settings**

	Developers can write different configuration settings for different environments in separated .cfg files. I wrote separate configurations for development, testing, and production environments.

- **Modular design (with packages and Flask Blueprints)**

	Effective implementation of DRY coding and  separation of concerns. Routes are separated into their own flask blueprints and packages for importing and and linking to a Flask application. SQLAlchemy models are separated into packages.

- **Additional Tools Used**

	 Pytest, SQLAlchemy, Flask Praetorian

## Local Installation - Requirements
Core:
- Python3
- pip
- PostgreSQL

Highly Recommended:
- Bash shell. Mac/Linux users should already come with a UNIX like Terminal. Windows users can try GitBash or WSL as options
- Insomnia (for testing REST API endpoints)

Generally Recommended:
- ipython (multi-use, versatile python REPL with syntax highlighting)


## Local Installation - Instructions:


1. **Clone the repository**

2. **Create a virtual environment with the name "venv**"

	`python -m venv venv`

	If this is your first time encountering the venv module or virtual environments, I highly recommend reading the 	Python docs or 	learning about them first.

4. **Activate the virtual environment:**

	`source venv/bin/activate`

	A different command may be required for windows users.
	Could possibly be:
	
	`source venv/Scripts/activate`

5. **Ensure your virtual environment is activated.**
	If you followed the previous instructions, you might see `(venv)` in your CLI.

6. **Install dependencies from the requirements.txt file**

	`pip install -r requirements.txt`

	You can verify installation by using the command

	`pip freeze`

	You should see a list of dependencies that matches the requirements.txt file.
	For quick visual comparison:

	`cat requirements.txt`

7. **Open PostgreSQL interactive terminal.**
	The command may differ depending on your system settings.
	Refer to PostgreSQL docs if you run into issues.

	From my (limited) knowledge, it could be one of the following:
	
	`psql`
	
	or...
	`psql -U postgres`
	
	or...
	`psql -U postgres postgres`

	There are implications behind each command. To better understand them, please refer to the PostgreSQL docs.

	Once you have PostgreSQL open... 

8. **Create the database:**

	`CREATE DATABASE forleti_db;`

	For testing environment, create the following database:

	`CREATE DATABASE forleti_db_test;`

9. **Exit PostgreSQL**

10. **Seed the tables in the database.**

	`python seed.py`

	...or if in ipython:

	`%run seed.py`


11. **Run flask server.** Your virtual environment should still be activated. If not, repeat step 4.

	Run the following command in your Terminal:

	`flask run`

	You can run flask in different environments. Refer to Flask docs for more info

	You should see the server running on localhost:5000. You can now utilize forleti REST API. Try the following in your browser:

	`localhost:5000/poke`
	You should receive the JSON message:

	`{"Poke you back!"}`

	*I recommend using Insomnia to test endpoints. Alternatively, there are browser plugins (e.g. RESTer) that you can use. Either way, you will need something that can send HTTP requests with a JSON body.*

**Hope this helps!**



## Running Tests:
Ensure testing database is created (instructions found above under STEP 8).

To run all tests, make sure you're in the root directory and run the following command:

`pytest`
