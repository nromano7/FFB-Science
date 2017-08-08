import nfldb

db = nfldb.connect()
q = nfldb.Query(db)

q.game(season_year=2016, season_type='Regular',team='PHI')
for game in q.as_games():
    print game

