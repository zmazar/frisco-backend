module BeerMod
    class Beer
        attr_accessor :name, :abv

        def initialize(name, abv)
            @name = name
            @abv = abv
        end
    end
end
