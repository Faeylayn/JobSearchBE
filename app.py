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

# class User(Base):
#     __tablename__ = 'User'
#     id = Column(Integer, primary_key=True)
#     UserName = Column(String(250), nullable=False)

class Listing(Base):
    __tablename__ = 'Listing'
    id = Column(Integer, primary_key=True)
    ListingName = Column(String(250), nullable=False)
    ListingCompany = Column(String(250), nullable=False)
    Link = Column(String(250), default=None)
    ResultPage = Column(Text(), default=None)
    Status = Column(String(250), default=None)

engine = create_engine('sqlite:///jobsearch.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

app = Flask(__name__)
CORS(app)
api = Api(app)
socketio = SocketIO(app)


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
    def get(self):
        try:

            try:
                listings = session.query(Listing).all()
            except NoResultFound:
                listings = []

            parsed_listings = []

            for listing in listings:
                temp_listing = {
                    'ListingName': listing.ListingName,
                    'ListingCompany': listing.ListingCompany,
                    'Link': listing.Link,
                    'Status': listing.Status,
                    'Id': listing.id
                }
                parsed_listings.append(temp_listing)
            return {
                'listings': parsed_listings
            }

        except Exception as e:
            return {'error': str(e)}

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ListingName', type=str, help='name of listing to be added to the db')
            parser.add_argument('ListingCompany', type=str, help='company of listing to be added to the db')
            parser.add_argument('Link', type=str, help='the muse link of listing to be added to the db')
            parser.add_argument('ResultPage', type=str, help='html of listing to be added to the db')

            args = parser.parse_args()

            listing = session.query(Listing).filter(Listing.ListingName == args['ListingName']).first()

            if listing is not None:
                return {"Message": "Existing User"}
            else:
                new_listing = Listing(ListingName=args['ListingName'], ListingCompany=args['ListingCompany'],
                    Link=args['Link'], ResultPage=args['ResultPage'])
                session.add(new_listing)
                session.commit()

            return {'listing': 'success'}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(Listings, '/listings')



if __name__ == '__main__':
    socketio.run(app)
