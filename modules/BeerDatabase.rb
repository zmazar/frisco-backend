require "dbi"
require "./modules/BeerMod"

USER = "friscoapp"
PASS = "friscotapAPPLE"

module BeerDatabase
    class BeerDb
        attr_accessor :dbh, :table_name

        def initialize(table)
            @table_name = table
        end

        def connect()
            begin
                # connect to the DB
                @dbh = DBI.connect(
                    "DBI:Mysql:beer_db:localhost", 
                    USER, 
                    PASS
                )

                puts "Connected to beer_db"
            rescue DBI::DatabaseError => e
                puts "An error occurred"
                puts "Error code:    #{e.err}"
                puts "Error message: #{e.errstr}"
            end
        end

        def disconnect()
            dbh.disconnect() if dbh
        end

        def beerdb_insert(beer)
            # As long as we have a connection to the database
            if @dbh
                begin
                    # Build INSERT statement
                    stmt = "INSERT INTO #{@table_name}(NAME, ABV, FRISCO_CLASS, TAP_DATE, FRISCO_ID) "
                    stmt += "VALUES(?, ?, ?, ?, ?)"

                    # Perform the query
                    sth = dbh.prepare(stmt)
                    sth.execute(beer.name, beer.abv, beer.frisco_class, beer.tap_time, beer.frisco_id)

                    sth.finish
                    dbh.commit
                rescue DBI::DatabaseError => e
                    puts "An error occurred"
                    puts "Error code:    #{e.err}"
                    puts "Error message: #{e.errstr}"
                end
            end
        end

        def beerdb_insert_all(beers)
            # As long as we have a connection to the database
            if @dbh
                begin
                    # Build INSERT statement
                    stmt = "INSERT IGNORE INTO #{@table_name}(NAME, ABV, FRISCO_CLASS, TAP_DATE, FRISCO_ID) "
                    stmt += "VALUES(?, ?, ?, ?, ?)"

                    # Prepare the query
                    sth = dbh.prepare(stmt)

                    beers.each_with_index do |beer, index|
                        sth.execute(beer.name, beer.abv, beer.frisco_class, beer.tap_time, beer.frisco_id)
                    end

                    sth.finish 
                    dbh.commit
                rescue DBI::DatabaseError => e
                    puts "An error occurred"
                    puts "Error code:    #{e.err}"
                    puts "Error message: #{e.errstr}"

                    dbh.rollback
                end
            end

        end
        def beerdb_get(beer)
            if @dbh
                begin
                    row = dbh.select_one("SELECT * FROM #{@table_name} WHERE NAME = #{beer.name}")
                    b = BeerMod::Beer.new(row[0], row[1], row[4])
                    b.set_taptime(row[5])
                    b.set_friscoid(row[2])

                    sth.finish
                rescue DBI::DatabaseError => e
                    puts "An error occurred"
                    puts "Error code:    #{e.err}"
                    puts "Error message: #{e.errstr}"
                end
            end

            return b
        end

        def beerdb_get_all()
            if @dbh
                begin
                    sth = dbh.prepare("SELECT * FROM #{@table_name}")
                    sth.execute()

                    # Setup list variable
                    beers_list = Array.new

                    sth.fetch do |row|
                        b = BeerMod::Beer.new(row[0], row[1], row[4])
                        b.set_taptime(row[5])
                        b.set_friscoid(row[2])

                        beers_list << b
                    end

                    sth.finish
                rescue DBI::DatabaseError => e
                    puts "An error occurred"
                    puts "Error code:    #{e.err}"
                    puts "Error message: #{e.errstr}"
                end

            end

            return beers_list
        end

        def beerdb_update()
        end

        def beerdb_delete(beer)
            # As long as we have a connection to the database
            if @dbh
                begin
                    # Build INSERT statement
                    stmt = "DELETE FROM #{@table_name} WHERE inv_id=?"

                    # Perform the query
                    sth = dbh.prepare(stmt)
                    sth.execute(beer.inv_id)

                    sth.finish
                    dbh.commit
                rescue DBI::DatabaseError => e
                    puts "An error occurred"
                    puts "Error code:    #{e.err}"
                    puts "Error message: #{e.errstr}"
                end
            end
        end
    end
end
