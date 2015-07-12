#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
       conn = psycopg2.connect("dbname=tournament")
       return conn
    except psycopg2.Error as e:
       print e

def get(command):
    """Creates cursor, executes command, commints changes"""
    db = connect()
    cursor = db.cursor()
    cursor.execute(command)
    db.commit()
    try:
        rows = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        rows = False
    db.close()
    if rows:
        return rows

def deleteMatches():
    """Remove all the match records from the database."""
    get("DELETE FROM Matches")


def deletePlayers():
    """Remove all the player records from the database."""
    get("DELETE FROM Players")


def countPlayers():
    """Returns the number of players currently registered."""
    rows = get("SELECT count(id) FROM Players;")
    return rows[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Players (name) VALUES (%s)",(name,))
    db.commit()
    db.close()


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
    rows = get("SELECT id,name,wins,matches FROM Standings ORDER BY wins DESC;")
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Matches (winner,loser) VALUES (%s,%s)",(winner,loser))
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
    count = playerStandings()
    i=0
    pairings = []
    while i < len(count):
        id1 = count[i][0]
        name1 = count[i][1]
        id2 = count[i+1][0]
        name2 = count[i+1][1]
        pairings.append((id1,name1,id2,name2))
        i += 2
    return pairings


