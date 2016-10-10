#!/usr/bin/python

import time
import BaseHTTPServer
import MySQLdb
import json
import cgi
import simplejson

# Server variables
HOST = "45.33.92.167"
PORT = 80

# Database variables
COLUMBIA_TABLE = "columbia"
CROFTON_TABLE = "crofton"
INVENTORY_TABLE = "inventory"
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

class InvBeer:
    def __init__(self, name, abv, inv_id, style, time, size, loc):
        self.name = name
        self.abv = abv
        self.inv_id = inv_id
        self.style = style
        self.timestamp = str(time)
        self.size = size
        self.location = loc

    def get_dict(self):
        bd = dict()
        bd['name'] = self.name
        bd['abv'] = self.abv
        bd['inv_id'] = self.inv_id
        bd['style'] = self.style
        bd['tap_time'] = self.timestamp
        bd['size'] = self.size
        bd['loc'] = self.location

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

            s.__getBeers(s, table_name)
        if s.path == '/crofton':
            print "Handling Crofton request"
            table_name = CROFTON_TABLE

            s.__getBeers(s, table_name)
        if s.path == '/inventory':
            print "Handling inventory request"
            table_name = INVENTORY_TABLE

            s.__getInventory(table_name)
    
    def do_POST(self):
        print "Handling POST"
        ctype = self.headers.getheader('content-type')

        if ctype == 'application/json':
            clen = int(self.headers.getheader('content-length'))
            data_string = self.rfile.read(clen)
            data = simplejson.loads(data_string)

            if self.path == '/addbeer':
                # Begin response
                self.send_response(200)
                self.end_headers()

                # Extract data elements
                name = data['name']
                abv = data['abv']
                style = data['style']
                size = data['size']
                loc = data['loc']

                # Create a inventory beer object
                new_beer = InvBeer(name, abv, 0, style, None, size, loc)

                # Write the beer into the database
                _writeInventoryBeer(new_beer)
            elif self.path == '/delbeer':
                # Begin response
                self.send_response(200)
                self.end_headers()

                # Extract inventory ID to delete
                inv_id = data['inv_id']

                _deleteInventoryBeer(inv_id)
    def __getBeers(self, s, table_name=None):
        # First, get data from the database
        beers_list = _readBeersFromDb(table_name)

        # Convert the list to a JSON array
        json_data = _convertToJSON(beers_list)

        # Construct the response
        s.send_response(200)
        s.send_header("Content-Type", "application/json")
        s.end_headers()

        s.wfile.write(json_data)

    def __getInventory(self, table_name):
        # Get the beers for the inventory list
        beers_list = _readInventoryFromDb(table_name)

        # Convert the list to a JSON array
        json_data = _convertToJSON(beers_list)

        # Construct the response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json_data)

def _readInventoryFromDb(table_name=None):
    beer_list = []

    # Connect to the database
    db = MySQLdb.connect(LOCALHOST, USER, PASS, BEER_DB)

    # Prepare a cursor to traverse the resulting rows
    cursor = db.cursor()

    # Execute a query to get all inventory
    query = "SELECT * FROM " + table_name
    cursor.execute(query)

    # Now fetch all of the rows from the resulting query
    beers = cursor.fetchall()
    
    for beer in beers:
        b = InvBeer(beer[0], beer[1], beer[2], beer[3], beer[4], beer[5], beer[6])
        print b.name
        beer_list.append(b)

    # Close the db
    db.close()

    print beer_list

    return beer_list

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

def _writeInventoryBeer(beer):
    # Connect to the database
    db = MySQLdb.connect(LOCALHOST, USER, PASS, BEER_DB)

    # Create a cursor for the db
    cursor = db.cursor()

    # Create SQL query
    sql = """INSERT INTO inventory(NAME, STYLE, ABV, SIZE, LOC) VALUES ('%s',%s,'%s',%s,%s)""" % (beer.name, beer.style, beer.abv, beer.size, beer.location)
    
    print "SQL Statement: " + sql
    # Insert into the table
    try:
        cursor.execute(sql)
        db.commit()
        print "Wrote %s to DB" % beer.name
    except MySQLdb.Error, e:
        print "Failed to insert beer into Inventory"
        print e
        #print "{0}: {1}".format(e.errno, e.strerror)
        db.rollback()

    db.close()

def _deleteInventoryBeer(inv_id):
    # Connect to the database
    db = MySQLdb.connect(LOCALHOST, USER, PASS, BEER_DB)

    # Create a cursor for the db
    cursor = db.cursor()

    # Create SQL query
    sql = """DELETE FROM inventory WHERE inv_id=%s""" % inv_id
    
    print "SQL Statement: " + sql

    # Delete from table
    try:
        cursor.execute(sql)
        db.commit()
        print "Deleted ID %s from DB" % inv_id
    except MySQLdb.Error, e:
        print "Failed to delete beer into Inventory"
        print e
        db.rollback()

    db.close()

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
