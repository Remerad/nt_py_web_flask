import atexit
from os import getenv
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, select
from flask.views import MethodView
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine(f"postgresql://postgres:{getenv('PG_pasw')}@127.0.0.1:5432/flask_netology", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
atexit.register(lambda: engine.dispose())


class AdvertisementModel(Base):
    __tablename__ = 'advertisements'
    id = Column(Integer, primary_key=True)
    heading = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all(engine)
app = Flask(__name__)


class AdvertisementView(MethodView):
    def post(self):
        json_data = request.json
        with Session() as session:
            try:
                advertisement = AdvertisementModel(
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

    def get(self):
        with Session() as session:
            try:
                statement = select(AdvertisementModel)
                ads_list = session.scalars(statement).all()
                results = []
                for ads in ads_list:
                    results.append (
                        {
                            "heading": ads.heading,
                            "description": ads.description,
                            "registration_time": ads.registration_time,
                            "owner": ads.owner
                        }
                    )
                return jsonify({"count": len(ads_list), "ads": results})
            except IntegrityError:
                response = jsonify({
                    'error': "Что-то пошло не так. Сделайте как-то по-другому."
                })
                response.status_code = 400
                return response

    def delete(self):
        json_data = request.json
        with Session() as session:
            try:
                statement = select(AdvertisementModel).filter_by(heading=json_data["heading"])
                ads_list = session.scalars(statement).all()
                for ads in ads_list:
                    session.delete(ads)
                session.commit()
                return jsonify({"Удалены сообщения с заголовком": json_data["heading"]})
            except IntegrityError:
                response = jsonify({
                    'error': "Что-то пошло не так. Сделайте как-то по-другому."
                })
                response.status_code = 400
                return response

app.add_url_rule('/advertisement/',
                 view_func=AdvertisementView.as_view('create_advertisement'),
                 methods=['POST', 'GET', 'DELETE'])
app.run(
    host='0.0.0.0',
    port=5500
)


