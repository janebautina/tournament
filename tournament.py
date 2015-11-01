#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2


def connect(database_name = "tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname = {}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Can't connect to the database") 


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    query = "DELETE FROM matches;"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "DELETE FROM players;"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "SELECT COUNT(*) AS count FROM players;"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO players(name, bye) VALUES(%s, FALSE);"
    parameter = (name,)
    cursor.execute(query, parameter)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    # result table as join winns view and matches table sorted by number of wins
    cursor.execute("select w.player_id as id, w.name, " +
        "w.wins,(count(m2.loser_id)+w.wins) as matches from winns w left outer " + 
        "join matches m2 on w.player_id=m2.loser_id group by player_id, w.name," +
        " w.wins order by wins")
    list = cursor.fetchall()
    db.close()
    return list


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "INSERT INTO matches(winner_id, loser_id) VALUES (%s,%s)"
    parameter = (winner, loser,)
    cursor.execute(query, parameter)
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    """Extra credit. Do not assume an even number of players. If there is an odd
    number of players, assign one player "bye" (skipped round). A bye counts as 
    a free win. A player should not receive more than one buy 
    in a tournament."""

    player_standings = playerStandings()
    db, cursor = connect()
    if countPlayers() == 0:
        print "Null"
    if countPlayers() % 2 != 0:   # odd number of players
        bye_player_id = 0   # player to say "bye"
        query = "SELECT player_id, bye FROM players;"
        cursor.execute(query)
        list = cursor.fetchall()
        # find player who did't recive "bye" before
        for row in list:
            if row[1] == 0:
                bye_player_id = row[0]
                break
        # update bye status to true or say him 'bye'
        cursor.execute("UPDATE players SET bye = TRUE WHERE player_id = " +
          str(bye_player_id))
        # his free win round
        # report new match with winer and loser ids as "bye" player id
        reportMatch(bye_player_id, bye_player_id) 
        # find  match' id of the winner equals loser match 
        cursor.execute("SELECT match_id FROM matches WHERE winner_id = loser_id")
        match_id = cursor.fetchone()[0]
        # change loser_id to null as it is free win match 
        cursor.execute("UPDATE matches SET loser_id = null WHERE match_id = "+
           str(match_id))
        db.commit()
        db.close()
        # delete him from a match
        player_standings = [s for s in player_standings if s[0] != bye_player_id]
    # return pairs of players with an equal or nearly-equal win record
    return [
        (standing_pair[0][0],
         standing_pair[0][1],
         standing_pair[1][0],
         standing_pair[1][1])
        for standing_pair in [
          player_standings[i:i+2] for i in xrange(0, len(player_standings), 2)
        ]
    ]
