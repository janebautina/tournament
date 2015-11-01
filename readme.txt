Welcome to Tournament project!

Tournament project realizes a tournament game that uses the Swiss system 
for pairing up players in each round: players are not eliminated, and each
 player should be paired with another player with the same number of wins, 
or as close as possible.

The project includes tournament.sql with tables' definitions and 
tournament.py game API realization.

Running instructions:
1. On Vagrant VM istall and configure PostgreSQL
2. Run and log into VM
3. Navigate to the directory where the files are located
4. Type the following command lines in the terminal
          psql
          \i tournament.sql
          \q
          python tournament_test.py
5. You should be able to see the following output:
   1. Old matches can be deleted.
   2. Player records can be deleted.
   3. After deleting, countPlayers() returns zero.
   4. After registering a player, countPlayers() returns 1.
   5. Players can be registered and deleted.
   6. Newly registered players appear in the standings with no matches.
   7. After a match, players have updated standings.   
   8. After one match, players with one win are paired.
   Success!  All tests pass!    
