Configuring flask application
-

Start virtual environment
-
1. Install python in machine.
2. Go to VSCode terminal.
3. Enter command as `python -m venv .venv`
4. Open setting, navigate to Select interpreter.
5. If it show venv excutable, select that. Ignore step-6 if this is successful.
6. If venv does not exist, go to enter interpreter path.
     Select "flask_store/.venv/Scripts/python.exe"
7. Bin the current terminal 
8. Open a new terminal 
9. The project will start with venv. e.g. Path in terminal will have "(.venv)" as start

## Run the flask app locally
1. Check if virtual environment is active. If not refer to above steps to start venv
2. Go to flask_store folder.
3. Run  `pip install -r requirements.txt` in terminal.
4. Start flask app with `flask run` this command.

# Docker image build and run
1. Check Dockerfile
2. Run command `docker build -t <image_name> .`
3. To run image enter `docker run -dp 5000:5000 <image_name>`

**Run  flask in docker containers**
1. Hot run the docker container.
    - Windows:
        `docker run -dp 5000:5000 -w /app -v "/c/Documents/yourproject:/app" flask-smorest-api`
    - Linux, MacOS:
        `docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api`
2. Build a docker image
    `docker build -t flask-smorest-api .`
3. Run container
    `docker run -dp 5000:5000 flask-smorest-api`

URL Details:
Rest url `http://127.0.0.1:5000/`
Swagger url `http://127.0.0.1:5000/swagger-ui`



# Notes:
1. "flask run" to start app.
    FLASK_APP=app >> tell env to check where the app is(python script to run)

2. The function called mentioned in FLASK_APP to start app
    app = Flask(__name__)

3. Can use different configs with app.config["<config_constants>"]

## Features:
1. Blueprints:
    1. Used for dividing API in different parts. api.register_blueprint(ItemBlueprint) >>> 'api' from flask_smorest
    2. blp = Blueprint("items", __name__, description= "Operation on items") >> will reflect to documentation
    3. Connection is via 'from flask.views import MethodView'
    4. Decorate the class with blp.route("<endpoint>")
        e.g.@blp.route("/store/<string:store_id>")
            class Store(MethodView):
    5. 

2. Schemas:
    1. Used for data validations from marshmallow
    2. It is used inside the resources along with blueprints. 
            @blp.arguments(ItemSchema)
            @blp.response(201, ItemSchema)
            def post(self, item_data): >>  item_data is a validated json from ItemSchema
    3. It reflects the swagger-ui docs
    4. Create class for each .. ItemSchema(Schema)
        Pass as attributes of class id = fields.Str(dump_only= True)
        dump_only >> Can we used to fetch data, but can not passed as parameter
        required >> Must is passed as parameter 
    5. Also, responses can we validated using blp.repsonse(200, ItemSchema) 
        Update docs with expected response for a response code

    
3. SQLAlchemy:
    1. Use SQLAlchemy as database management
    2. In the create_app in the app.py >> use db.init_app(app)
    3. db.py >> db = SQLAlchemy(). 
    4. In ItemModel >> db.Column(db.Integer, primary_key= True, .......) >> Data defination similar to SQL
        Foreign keys also can mentioned in the db.Column()
    5. Relationship between tables...
        Get store details (will fetch object of "StoreModel") from store table object
        store = db.relationship("StoreModel", back_populates="items")
    6. DML: ' StoreModel.query.get_or_404(store_id) ' 
        1. Insert Data: Uses POST
            db.session.add(item)
            db.session.commit()
            Raises IntegrityError if it breaks data consistency. i.e. Modeling of data defined in DDL
        2. Get data: Uses GET 
            item = ItemModel.query.get_or_404(item_id)
        3. Update data: uses PUT
            Idempotency: Same results for a same request. 
        4. Delete data: uses DELETE
            item = ItemModel.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
        5. List: use GET
            ItemModel.query.all()

4. JWT Authentication:
    1. 