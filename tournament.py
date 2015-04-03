#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    con = connect()
    DB = con.cursor()
    DB.execute("DELETE FROM matches;")
    con.commit()
    DB.close()
    con.close()


def deletePlayers():
    """Remove all the player records from the database."""
    con = connect()
    DB = con.cursor()
    DB.execute("DELETE FROM players;")
    con.commit()
    DB.close()
    con.close()


def countPlayers():
    """Returns the number of players currently registered."""
    con = connect()
    DB = con.cursor()
    DB.execute("SELECT count(*) FROM players;")
    players_count = DB.fetchall()[0][0]
    DB.close()
    con.close()
    return players_count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    con = connect()
    DB = con.cursor()
    cmd = "INSERT INTO players(name) VALUES (%s);"
    DB.execute(cmd,(name,))
    con.commit()
    DB.close()
    con.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    con = connect()
    DB = con.cursor()
    DB.execute("SELECT * FROM players ORDER BY wins DESC;")
    players_stand = DB.fetchall()
    print players_stand
    DB.close()
    con.close()
    return players_stand


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    con = connect()
    DB = con.cursor()
    sql = ("UPDATE players SET wins = wins + 1, matches = matches + 1 WHERE id = %s;")
    data = (winner,)
    DB.execute(sql,data)
    sql1 = ("UPDATE players SET matches = matches + 1 WHERE id = %s;")
    data1 = (loser,)
    DB.execute(sql1,data1)
    con.commit()
    DB.close()
    con.close()



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
    con = connect()
    DB = con.cursor()
    DB.execute("SELECT id,name FROM players ORDER BY wins DESC;")
    players_test = DB.fetchall()
    duzina = len(players_test)
    a = 0
    next_matches = []
    while a < duzina:
        next_match = players_test[a] + players_test[a+1]
        a = a + 2
        next_matches.append(next_match)
    DB.close()
    con.close()
    return next_matches
