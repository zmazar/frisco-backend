module BeerMod
    class Beer
        attr_accessor :name, :abv, :frisco_class, :tap_time, :frisco_id

        def initialize(name, abv, beer_class)
            @name = name
            @abv = abv
            @frisco_class = beer_class
        end

        def set_taptime(time)
            @tap_time = time
        end

        def set_friscoid(fid)
            @frisco_id = fid
        end
    end
end
