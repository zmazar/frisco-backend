#!/usr/bin/ruby

require 'mechanize'
require 'rubygems'
require 'active_support/all'
require './modules/BeerMod'
require './modules/BeerDatabase'

COLUMBIA_URL = 'http://www.friscogrille.com/cmobile-alt.php'
CROFTON_URL = 'http://www.friscogrille.com/wcmobile-alt.php'
COLUMBIA_TABLE = "columbia"
CROFTON_TABLE = "crofton"

module Frisco
    def self.beers(url, table)
        spider = Mechanize.new { |agent|
            agent.user_agent_alias = 'Windows Mozilla'
        }

        beers = []
        abvs = []
        page = spider.get(url)

        page.search('.row > .sixteenounce > .name').each do |beer|
            beers << beer.text
        end

        page.search('.row > .sixteenounce > .abv').each do |abv|
            abvs << abv.text
        end

        page.search('.row > .tenounce > .name').each do |beer|
            beers << beer.text
        end

        page.search('.row > .tenounce > .abv').each do |abv|
            abvs << abv.text
        end

        page.search('.row > .eightounce > .name').each do |beer|
            beers << beer.text
        end

        page.search('.row > .eightounce > .abv').each do |abv|
            abvs << abv.text
        end

        beers_list = Array.new

        puts "Frisco Taphouse / Beers:"
        beers.each_with_index do |beer, index|
            b = BeerMod::Beer.new(beer, abvs[index])
            beers_list << b
        end

        # Insert the beer list into the table
        db = BeerDatabase::BeerDb.new(table)
        db.connect()

        db.beerdb_insert_all(beers_list)

        beers_list2 = db.beerdb_get_all()

        db.disconnect()

        beers_list2.each do |beer|
            puts "#{beer.name} #{beer.abv}"
        end
    end
end

Frisco.beers(COLUMBIA_URL, COLUMBIA_TABLE)
#Frisco.beers(CROFTON_URL, CROFTON_TABLE)
