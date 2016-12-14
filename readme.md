This is a basic single chatroom app that stores the entire chat log to a local db.

This utilizes Flask to create the API for an angular frontend app located in
the Job-Search repository

#Installation

All that needs to be done is run
pip install -r requirements.txt

following that simply run python app.py

#Endpoints
The app utilizes 3 endpoints:

##/LoginUser
This will either login the user if it is existing, or create a new user if it does
not exist and then login the user. It takes UserName as a parameter
