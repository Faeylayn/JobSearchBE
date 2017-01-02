from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import sqlite3
import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    UserName = Column(String(250), nullable=False)

class Listing(Base):
    __tablename__ = 'Listing'
    id = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey(User.id), nullable=False)
    ListingName = Column(String(250), nullable=False)
    ListingCompany = Column(String(250), nullable=False)
    Link = Column(String(250), nullable=False)
    ResultPage = Column(Text(), nullable=False)

engine = create_engine('sqlite:///jobsearch.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

app = Flask(__name__)
CORS(app)
api = Api(app)
socketio = SocketIO(app)
#
# epoch = datetime.datetime.utcfromtimestamp(0)
#
# def unix_time_millis(dt):
#     return (dt - epoch).total_seconds() * 1000.0

# class LoginUser(Resource):
#     # may need this if we decide to make users and auth a thing
#     def post(self):
#         try:
#             parser = reqparse.RequestParser()
#             parser.add_argument('UserName', type=str, help='user_name address to lookup/create user')
#             args = parser.parse_args()
#
#             user_name = args['UserName']
#             user = session.query(User).filter(User.UserName == user_name).first()
#             if user is not None:
#                 return {"Message": "Existing User"}
#             else:
#                 new_person = User(UserName=user_name)
#                 session.add(new_person)
#                 session.commit()
#
#             return {'user_name': user_name}
#
#         except Exception as e:
#             return {'error': str(e)}
#
# api.add_resource(LoginUser, '/LoginUser')

class Listings(Resource):
    # may need this if we decide to make users and auth a thing
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('UserId', type=int, help='user_id address to relate listing to user')
            args = parser.parse_args()

            user_id = args['UserId']

            try:
                listings = session.query(Listing).filter(Listing.UserId == user_id).all()
            except NoResultFound:
                listings = []
            return {
                'user_id': user_id,
                'listings': listings
            }

        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('UserId', type=int, help='user_id address to relate listing to user')
            parser.add_argument('Listing', type=int, help='listing to be added to the db')
            args = parser.parse_args()

            user_id = args['UserId']

            new_listing = Listing(UserId=user_id, )
            session.add(new_listing)
            session.commit()

            return {'user_id': user_id}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(Listings, '/listings')



if __name__ == '__main__':
    socketio.run(app)
