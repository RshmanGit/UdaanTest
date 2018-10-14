from flask import Flask, request, render_template, url_for, redirect, jsonify, abort
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbSetup.database_setup import Base

from dbSetup import database_setup
from dbSetup.serveCreds import serve

from views.screenInfo import *

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

###################################################################
#Main Route to enter screens into the database
###################################################################
@app.route('/screens/', methods=['GET','POST'])
def addScreen():
    if(request.method == "POST"):
        data = request.get_json()

        result = addNewScreen(data)

        if(result):
            return jsonify({"status": "finished adding"})
        else:
            return jsonify({'Status': "adding failed"})

    if(request.method == "GET"):
        abort(405)

###################################################################
#Main route to reserve seats
###################################################################
@app.route('/screens/<string:screenName>/reserve', methods=['GET', 'POST'])
def reserveSeats(screenName):
    if(request.method == "POST"):
        data = request.get_json()
        res = reserveSeatsFor(screenName, data)
        if(res):
            return jsonify({"status": "reserved"})
        else:
            return jsonify({"status": "unknown screen or prereserved seats"})
    if(request.methos == "GET"):
        abort(405)


###################################################################
#To fetch all unreserved seats To fetch all unreserved seats
###################################################################
@app.route('/screens/<string:screenName>/seats', methods=["GET", "POST"])
def unReservedSeats(screenName):
    if(request.method == "GET"):
        data = request.args.get('status')
        numSeats = request.args.get('numSeats')
        choice = request.args.get('choice')

        if(data == "unreserved"):
            result = {}
            result = fetchUnreservedSeats(screenName)
            return jsonify(seats = result)
        if(numSeats and choice):
            result = fetchOptimalSeats(screenName, numSeats, choice)
            if(result):
                return jsonify(availableSeats = result)
            else:
                return jsonify({"Error": "Seats Invalid or contigous"})

        else:
            return jsonify({'status': 'unknown args'})
    if(request.method == "POST"):
        abort(405)


if __name__ == "__main__":
    app.debug = True
    database_setup.run()
    app.run(host = '0.0.0.0', port=9090)