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

        beers16 = []
        beers10 = []
        beers8 = []
        abvs16 = []
        abvs10 = []
        abvs8 = []
        page = spider.get(url)

        # Scrape the page for 16oz beers
        page.search('.row > .sixteenounce > .name').each do |beer|
            beers16 << beer.text
        end

        page.search('.row > .sixteenounce > .abv').each do |abv|
            abvs16 << abv.text
        end

        # Scrape the page of 10oz beers
        page.search('.row > .tenounce > .name').each do |beer|
            beers10 << beer.text
        end

        page.search('.row > .tenounce > .abv').each do |abv|
            abvs10 << abv.text
        end

        # Scrape the page for Special beers
        page.search('.row > .eightounce > .name').each do |beer|
            beers8 << beer.text
        end

        page.search('.row > .eightounce > .abv').each do |abv|
            abvs8 << abv.text
        end

        beers_list = Array.new

        # Insert 16oz beers into the beer list
        beers16.each_with_index do |beer, index|
            b = BeerMod::Beer.new(beer, abvs16[index], 1)
            beers_list << b
        end

        # Insert 10oz beers into the beer list
        beers10.each_with_index do |beer, index|
            b = BeerMod::Beer.new(beer, abvs10[index], 2)
            beers_list << b
        end

        # Insert Special beers into the beer list
        beers8.each_with_index do |beer, index|
            b = BeerMod::Beer.new(beer, abvs8[index], 3)
            beers_list << b
        end

        # Insert the beer list into the table
        db = BeerDatabase::BeerDb.new(table)
        db.connect()
        db.beerdb_insert_all(beers_list)
        db.disconnect()
    end
end

Frisco.beers(COLUMBIA_URL, COLUMBIA_TABLE)
Frisco.beers(CROFTON_URL, CROFTON_TABLE)
