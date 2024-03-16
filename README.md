# Personal-Dashboard
Custom dashboard I have built to keep track of major stocks and news data across primarily 4 different countries:
Germany, US, UK, and India

TODO: Weather, Exchange Rates

## Technologies
Python, SQLAlchemy, Postgresql, Docker and Plotly Dash

## Functional Requirements
1. Extract, load and display stock and news data from the countries I am interested in
2. Data only has to be refreshed every day
3. 

## Non-functional requirements
1. Quick development speed
2. Portable i.e. it can run on various different systems
3. Maintainable hence adequate documentation for each function is important
4. Industry standard technologies i.e. so that I can show employable skills to a future employer

## Extraction and Transformation

1. Retrieve API keys from _ini_ file using Configparser. _api_keys.ini_ file is in _gitignore_ for security reasons.
2. Make API GET request using the API keys to get the data
3. Transform data: column renamings and parsing dates using datetime module and dictionary comprehensions.
4. Logging and exception handling throughout the function in order to have more descriptive and helpful error messages for example when response status code is not 200 etc

## Loading data

1. Define Python dataclasses which will then be mapped to relations/tables in the database. Each dataclass will contain the table name, attributes which are defined as Sqlalchemy columns with types, and the primary key(s) is/are specified. 
2. SQLAlchemy is an object relational mapper which means it is able to convert Python classes into relations by automatically generating the SQL DDL i.e. CREATE TABLE ..., in order to generate the tables. I make sure that we create a Base class which is intialized to the Sqlalchemy declarative base and ensure that every Python dataclass inherits this Base class.
3. Create a database Engine object to establish a connection with the database using the details retrieved from the _database.ini_ file. 
4. Create the actual tables by doing _Base.metadata.create_all(engine.db_engine)_
5. Insert data by creating a database session using the engine and then using the session with a context manager. Then use _session.add()_ to actually insert the data into the tables. Make sure to query the tables before inserting to make sure we don't insert duplicate data with the same primary key.


## Visualization

1. Create basic layout using Plotly Dash which involves creating dcc (dash core components) e.g. tabs, and html divs
2. Added styling to components using inline CSS e.g. _style={"display": "flex", "margin": "auto", "width": "1800px", "justify-content": "space-around"}_
3. Created callback functions to add interactivity i.e. clicking buttons. A callback function takes in an _Input_ component which contains its id and its _value_ attribute, and then a callback function also takes in an _Output_ component which contains the id and its _children_ attribute. Then within the callback function we can specify how a change in the _Input_ would affect the _children_ attribute _Output_

## Containerization
1. Wrote _docker-compose.yaml_ file to specify how to build the images and run the containers. _docker-compose_ is a more streamlined and cleaner way of defining multiple containers, their dependencies and a common network for the containers to communicate between eachother. This is much cleaner than writing individual commands in a _Dockerfile_.
2. Specified the ports of the various containers correctly
3. Create Dockerfile to specify how to build the image for the python app i.e. installing dependencies e.g. _FROM python:3.10-slim_ to download Python base image, _COPY . ./_ copies the files from local directory to the container, _RUN pip install -r requirements.txt_ to install the pip dependencies
4. Configure the pythonapp container to only run once the database is ready to accept connections. To do this, I added a _healthcheck_ to the database container in the _docker-compose.yaml_ file. This healthcheck basically involves invoking a _pg-isready_ command every 5 seconds. Then in my python app container, I configure it to depend on the database container being healthy by doing _depends_on: pgdatabase: condition: service_healthy_
5. Add command to pythonapp container so it keeps running and runs the pipeline script once. This command in the _docker-compose.yaml_ file is _command: bash -c "python3 ./src/pipeline/run.py && tail -f /dev/null"_

## Integration testing
1. Use patch and Mock to mock an API GET request response so we can focus on testing the transformation part of the method
2. Created a Python class which inherits from _unittest.TestCase_ and add the decorator _@patch('requests.get')_ to mock this method  and created a mock object and specified the return value for this mock object

## Good coding practise
1. Makefile for common commands such as test, up, etc
2. isort to sort imports
3. format using black

## CI -  GitHub Actions
1. Create a _ci.yaml_ file inside of a _.github/workflows_ folder.
2. Specify the name as _CI_, what triggers it using _on: [pull_request]_, and then the jobs which each involve steps such as spinning up the containers, then running a _make ci_ command which involves sorting imports, formatting and executing the unit/integration tests. 



