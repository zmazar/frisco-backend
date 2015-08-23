#!/usr/bin/python

import time
import BaseHTTPServer
import MySQLdb
import json

# Server variables
HOST = "45.33.92.167"
PORT = 80

# Database variables
COLUMBIA_TABLE = "columbia"
CROFTON_TABLE = "crofton"
BEER_DB = "beer_db"
USER = "friscoapp"
PASS = "friscotapAPPLE"
LOCALHOST = "localhost"

class Beer:
    name = ""
    abv = ""
    frisco_class = 0
    timestamp = ""
    frisco_id = 0

    def __init__(self, name, abv, cls, time, fid):
        self.name = name
        self.abv = abv
        self.frisco_class = cls
        self.timestamp = str(time)
        self.frisco_id = fid

    def get_dict(self):
        bd = dict()
        bd['name'] = self.name
        bd['abv'] = self.abv
        bd['frisco_class'] = self.frisco_class
        bd['tap_time'] = self.timestamp
        bd['frisco_id'] = self.frisco_id

        return bd

class beerHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-Type", "text/html")
        s.end_headers()

    def do_GET(s):
        # Respond to GET requests
        table_name = ""

        if s.path == '/columbia':
            print "Handling Columbia request"
            table_name = COLUMBIA_TABLE
        if s.path == '/crofton':
            print "Handling Crofton request"
            table_name = CROFTON_TABLE

        # First, get data from the database
        beers_list = _readBeersFromDb(table_name)

        # Convert the list to a JSON array
        json_data = _convertToJSON(beers_list)

        # Construct the response
        s.send_response(200)
        s.send_header("Content-Type", "application/json")
        s.end_headers()

        s.wfile.write(json_data)
       
def _readBeersFromDb(table_name):
        beer_list = []

        # Connect to the database
        db = MySQLdb.connect(LOCALHOST, USER, PASS, BEER_DB)

        # Prepare a cursor to traverse the resulting rows
        cursor = db.cursor()

        # Execute a query to get all the beers in the specified table
        query = "SELECT * FROM " + table_name
        cursor.execute(query)
     
        # Now fetch all of the rows from the resulting query
        beers = cursor.fetchall()

        for beer in beers:
            b = Beer(beer[0], beer[1], beer[4], beer[5], beer[2])
            beer_list.append(b)
        
        # Close the db
        db.close()

        return beer_list

def _convertToJSON(beer_list):
    beer_array = []

    # For each beer in the list:
    #   1) Convert to a dictionary
    #   2) Append it to a new beer array
    for b in beer_list:
        beer_dict = b.get_dict()
        beer_array.append(beer_dict)

    beer_data = {'beer_data' : beer_array}

    # Return the Json encoded array
    return json.dumps(beer_data)

if __name__ == '__main__':
    server = BaseHTTPServer.HTTPServer

    httpd = server((HOST, PORT), beerHttpHandler)

    print time.asctime(), "Server started - %s:%s" % (HOST, PORT)

    httpd.serve_forever()
