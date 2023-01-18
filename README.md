Configuring flask application
----------------------------

Start virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install python in machine
2. Go to VSCode terminal
3. Enter command as `python -m venv .venv`
4. Open setting, navigate to Select interpreter
5. If it show venv excutable, select that. Ignore step-6 if this is successful
6. If venv does not exist, go to enter interpreter path.
    > Select "flask_store/.venv/Scripts/python.exe"
7. Bin the current terminal 
8. Open a new terminal 
9. The project will start with venv. e.g. Path in terminal will have "(.venv)" as start



Run the flask app
~~~~~~~~~~~~~~~~~

1. Check if virtual environment is active. If not refer to above steps to start venv
2. Go to flask_store folder.
3. Run  `pip install -r requirements.txt` in terminal.
4. Start flask app with `flask run` this command.


Docker image build and run
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Check Dockerfile
2. Run command `docker build -t <image_name> .`
3. To run image enter `docker run -dp 5000:5000 <image_name>`

Run docker container

1. Hot run the docker container.

Windows:
        `docker run -dp 5000:5000 -w /app -v "/c/Documents/yourproject:/app" flask-smorest-api`
        
Linux, MacOS:
        `docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api`

2. Build a docker image
    `docker build -t flask-smorest-api .`
3. Run container
    `docker run -dp 5000:5000 flask-smorest-api`


Documentation:
Rest url `http://127.0.0.1:5000/`
Swagger url `http://127.0.0.1:5000/swagger-ui`