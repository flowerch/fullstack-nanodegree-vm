#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2

from psycopg2 import connect

import itertools

import pdb

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect('dbname="tournament" user="dbuser" host="localhost" password="dbpass"')
    except:
        print "Connect to the database"
    
def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    query = "TRUNCATE matches"
    cur.execute(query)
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    query = "DELETE FROM players"
    cur.execute(query)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    query = "SELECT count(*) AS num FROM players"
    cur.execute(query)
    players_count = c.fetchone()[0]
    conn.commit()
    conn.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player. (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
    name: the player's full name (need not be unique).
    """
    conn = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    cur.execute = (query, parameter)
    conn.commit()
    conn.close()

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
    conn = connect()
    query = ("SELECT id, name, COUNT(matches.winner) AS wins, "
             "(SELECT games FROM games_view WHERE games_view.id = players.id) "
             "FROM players LEFT JOIN matches "
             "ON players.id = matches.winner "
             "GROUP BY players.id, players.name "
             "ORDER BY wins DESC")
    cur.execute(query)
    playerStandings = c.fetchall() #Fetches all remaining rows of a query result, returning a list.
    conn.close()
    return playerStandings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
    winner: the id number of the player who won
    loser: the id number of the player who lost
    """
    conn = connect()
    query = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)"
    parameter = (winner, loser)
    cur.execute(query, parameter)
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # For pairingsiterator relied on the recipes section of Python's
    # itertools docs: https://docs.python.org/2/library/itertools.html
    # and the Python Standard Library

    # Iterate through the list and build the pairings
  
    standings = playerStandings()
    pairingsiterator = itertools.izip(*[iter(standings)]*2)
    results = []
    pairings = list(pairingsiterator)
    for pair in pairings:
        id1 = pair[0][0]
        name1 = pair[0][1]
        id2 = pair[1][0]
        name2 = pair[1][1]
        matchup = (id1, name1, id2, name2)
        results.append(matchup)
    return results
