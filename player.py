from sheets import get_player_sheet as player_sheet

key_col_index = {
    "name": 1,
    "join_date": 2,
    "rank": 3,
    "events_attended": 4,
    "events_hosted": 5,
    "times_capped": 6,
    "total_points": 7,
    "last_event": 8,
    "last_cap": 9,
    "recruited_by": 10
}

num_cols = [
    "events_attended",
    "events_hosted",
    "times_capped",
    "total_points"
]


class Player:
    def new( name: str, date: str, recruited_by=None ):
        sheet = player_sheet()
        player = Player()

        # fill row with default values
        row = sheet.append_row( [
            name,
            date,  # join_date
            "01 Recruit",  # rank
            0,  # events_attended
            0,  # events_hosted
            0,  # times_capped
            0.00,  # total_points
            "",  # last_event
            "",  # last_cap
            ""  # recruited_by
        ], "USER_ENTERED" )

        # re-find the row and cache it
        player._row = sheet.find( name ).row

        return player

    def find( name ):
        target_row = player_sheet().find( name ).row

        player = Player()
        player._row = target_row

        return player

    def delete( self ):
        player_sheet().delete_row( self._row )

    def __getattr__( self, key ):
        if key in key_col_index:
            value = player_sheet().cell( self._row, key_col_index[key] ).value

            if key in num_cols:
                return float( value )
            else:
                return value
        else:
            raise AttributeError( "%r object has no attribute %r" %
                                  ( self.__class__.__name__, key ) )

    def __setattr__( self, key, value ):
        if key in key_col_index:
            player_sheet().update_cell( self._row, key_col_index[key], value )
        else:
            object.__setattr__( self, key, value )

    def __str__( self ):
        return "Player(" + \
            "name=" + self.name + ", " + \
            "join_date=" + self.join_date + ", " + \
            "rank=" + self.rank + ", " + \
            "events_attended=" + str( self.events_attended ) + ", " + \
            "events_hosted=" + str( self.events_hosted ) + ", " + \
            "times_capped=" + str( self.times_capped ) + ", " + \
            "total_points=" + str( self.total_points ) + ", " + \
            "last_event=" + self.last_event + ", " + \
            "last_cap=" + self.last_cap + \
            "recruited_by=" + self.recruited_by + \
            ")"
