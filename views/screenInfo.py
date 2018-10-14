from dbSetup.database_setup import Base, screen, row, seat
from dbSetup.serveCreds import serve

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import datetime
import time

engine = create_engine(serve())
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

def strTimeStamp():
    return str(datetime.datetime.today())

def addNewScreen(data):
    try:
        
        session = DBSession()

        screenName = data['name']
        newScreen = screen(name = screenName)
        rows = []

        srows = data['seatInfo']
        for srow in srows:
            newRow = row(name = str(srow))
            numberOfSeats = srows[srow]['numberOfSeats']
            aisleSeats = srows[srow]['aisleSeats']

            for sseat in range(numberOfSeats):
                if(sseat in aisleSeats):
                    newSeat = seat(number = sseat, aisle = True)
                    newRow.seats.append(newSeat)
                else:
                    newSeat = seat(number = sseat)
                    newRow.seats.append(newSeat)

            newScreen.rows.append(newRow)

        session.add(newScreen)
        session.commit()

        return True

    except Exception as e:
        print e
        return False
