import atexit
import psycopg2
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from flask.views import MethodView
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine(f"postgresql://postgres:postgres@127.0.0.1:5433/flask_netology", echo=True)#o12KinvJdE {getenv('PG_pasw')}
Base = declarative_base()
Session = sessionmaker(bind=engine)
atexit.register(lambda: engine.dispose())


class Advertisement(Base):
    __tablename__ = 'advertisements'
    id = Column(Integer, primary_key=True)
    heading = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all(engine)
app = Flask(__name__)


class AdvertisementView(MethodView):
    def get(self):
        json_data = request.json
        with Session() as session:
            try:

                session.query(Advertisement).all()
                # return jsonify({
                #     'heading': advertisement.heading,
                #     'description': advertisement.description,
                #     'owner': advertisement.owner,
                #     'registration_time': advertisement.registration_time.isoformat()
                # })
                print
            except IntegrityError:
                response = jsonify({
                    'error': "Что-то пошло не так. Сделайте как-то по-другому."
                })
                response.status_code = 400
                return response

    def post(self):
        json_data = request.json
        #json_data_validated = UserCreateModel(email=json_data['email'], password=json_data['password'])#.dict()
        with Session() as session:
            try:
                advertisement = Advertisement(
                    heading=json_data['heading'],
                    description=json_data['description'],
                    owner=json_data['owner']
                )
                session.add(advertisement)
                session.commit()
                return jsonify({
                    'heading': advertisement.heading,
                    'description': advertisement.description,
                    'owner': advertisement.owner,
                    'registration_time': advertisement.registration_time.isoformat()
                })
            except IntegrityError:
                response = jsonify({
                    'error': "Что-то пошло не так. Сделайте как-то по-другому."
                })
                response.status_code = 400
                return response


app.add_url_rule('/advertisement/',
                 view_func=AdvertisementView.as_view('create_advertisement'),
                 methods=['POST'])
app.run(
    host='0.0.0.0',
    port=5500
)


