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

def reserveSeatsFor(screenName, data):
    try:
        seats = data['seats']

        session = DBSession()

        fetchedScreen = session.query(screen).filter_by(name = str(screenName)).one()
        rows = {}
        for eachRow in fetchedScreen.rows:
            rows[eachRow.name] = eachRow

        for row in seats:
            if(row in rows):
                for seatNumber in seats[row]:
                    sseat = session.query(seat).filter_by(row = rows[row], number = seatNumber).one()
                    if(sseat.booked == False):
                        sseat.booked = True
                    else:
                        return False
            else:
                return False

        session.commit()
        return True
    except Exception as e:
        print e
        return False

def fetchUnreservedSeats(screenName):
    try:

        session = DBSession()

        rowsInScreen = {}
        sscreen = session.query(screen).filter_by(name = screenName).one()
        srowsInScreen = session.query(row).filter_by(screen = sscreen).all()
        for srow in srowsInScreen:
            rowsInScreen[srow.name] = srow

        rows = {}
        for srow in rowsInScreen:
            rows[srow] = []
            sseat = session.query(seat).filter_by(row = rowsInScreen[srow], booked = False).all()
            for iseat in sseat:
                rows[srow].append(iseat.number)

        session.commit()
        return rows

    except Exception as e:
        print(e)
        return None

def renderChoice(choice):
    return [str(choice[0]), int(choice[1:])]


def fetchOptimalSeats(screenName, numSeats, choice):
    try:
        rowName, startSeat = renderChoice(choice)
        result = {}

        session = DBSession()

        selectedScreen = session.query(screen).filter_by(name = screenName).one()
        selectedRow = session.query(row).filter_by(screen = selectedScreen, name = rowName).one()
        result[selectedRow.name] = []

        seats = {}
        seatsInRow = session.query(seat).filter_by(row = selectedRow).all()
        for sseat in seatsInRow:
            temp = [False] * 2
            temp[0] = sseat.booked
            temp[1] = sseat.aisle
            seats[sseat.number] = temp

        rowLength = len(seatsInRow)
        if(rowLength-int(numSeats) < startSeat):
            return False

        aisleSeats = []
        for i in seats:
            if(seats[i][1]):
                aisleSeats.append(i)

        for s in aisleSeats:
            if(s in range(startSeat+1, startSeat+int(numSeats)-1)):
                return False
        
        result[selectedRow.name] = range(startSeat, startSeat+int(numSeats))

        return result
    except Exception as e:
        print(e)
        return None