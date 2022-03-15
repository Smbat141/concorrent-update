# Simple REST Python web server

    1. DB - redis
    2. Server flask
    3. Test - pytest
    4. Environment - pipenv

### Install

    We use Docker to make installation easier
    Just run ```docker-compose up``` to install all required images

### Endpoints

    You can use "sayollo.postman_collection.json" file to import
    postman endpoints or use following endpoints
    
    1. localhost:5000/ad
          required params - sdk_version', 'session_id', 'platform', 'username', 'country_code
          return external api response(xml) and calulates requests for username and sdk
    2. localhost:5000/impression  
          required params - sdk_version', 'session_id', 'platform', 'username', 'country_code
          return json with success message and calulates requests for username and sdk

    3. localhost:5000/statistics  
          required params - username -> Jack or sdk -> 1.0
          return statistics by filter as json

### Structure

    Every endpoint logic located on its own directory.
    For packages information check Pipfile
    
    Flask
    In this task, we used flask because we did have not much functionality for Django rest, and flask covered all our needs for creating our endpoints. We also can use FastAPI or AIOHTTP, but the async solution can be not very effective because most of our functionality is related to calculations but we need some more complex investigation to understand async solutions' efectivity.
    
    Redis
    As Database, we used Redis because
        1. Redis save data in ram and it is fast (can also write data in file for persistence data)
        2. Redis supports data structures like a dictionary
        3. Redis is a single thread and we will have not data racing if we use Redis relevant functions.

    Other Databases
    Alternatively, we can use for instance relational database, add locks for avoiding data racing and have indexes for analytics, or have separated from Main DB solutions for analytics, for understanding exactly the right solution we need more information about the app and business logic also do more complex investigations related with performance and load

### Endpoint Validation

    permitted_parameters = [params...]
    
    To set required parameters just define permitted_params for 
    endpoint class as class attribute(if not all upcoming params are allowed)
    
    filter_permitted_parameters = [params...]

    same as for filter_permitted_parameters
    
    Note
        only FIRST matched param will be considered as filter param

# Tests

    to run tests just run ```docker-compose run sayollo pytest tests/ -v```

# Test concurrent incrementation

    1. pipenv shell
    
    2. set env variables
        export PYTHONPATH=.
        export FLASK_APP=main.py
    3. flask run
    
    4. run test_request_increment.py and test_request_increment.py
       in two seperate terminals(one will also be enough, but two only for different processes)
    
    5. check data using /statistics enpoind

# TODO

    1. I used custom request to validate params,
       but validation just cheking permitted_params(class attribute).
       For example validation not checks param values like in statistics filter
    2. Tests do not cover all cases and are not divided by concerns
    3. Vast external api can be defined as ENV variable
    4. For having persistence data in Redis we can add volume to Redis service and turn on the append-only function
    5. To have more complex functionality in Redis we can use Lua script and add custom functions to Redis
    6. To have more high load and/or complex analytics we can transform data and then move it to a more relevant database for analytics like AWS redshift
