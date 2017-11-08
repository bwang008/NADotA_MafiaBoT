==============================================================================================
=============================    INSTRUCTIONS        =========================================
==============================================================================================

1. To start a new game, delete the contents of config.txt (Or delete the file itself? I can't remember... If you delete the file make sure you back it up somewhere incase I was wrong lol). The bot will recreate the file once it goes through a thread (Maybe...)

config.txt serves as a record for the game the bot saw, so it does not look over the same pages/posts more than once. Deleting config.txt is not a big deal, the bot can be re-run except it will step through all posts again. This can take a few minutes in a very large game. 

2. Run MafiaBot.py to start the bot, it will check the Mafia forum automatically for a thread with the [ONGOING] tag. You can also enter the thread page directly into the config.txt file. 

==============================================================================================
==============================================================================================
==============================================================================================

	General Commands (Everyone can use):
[b]LYNCH #Player#[/b] - Places a lynch vote onto someone
[b]VOTECOUNT[/b] - Requests the bot to post the most recent vote count

	Host Commands:
[b]NIGHT BEGINS[/b] - Begins night phase, resets votes
[b]DAY BEGINS[/b] - Begins day phase, bot begins to count votes
[b]#Player# WAS KILLED[/b] - Removes a player from the bot's pool of valid voters
[b]KILL #player#[/b] - Same as above.
[b]ADD #Player#[/b] - Adds a player to the bot's pool of valid voters

	Example:
[b]KILL Ironstove.[/b] - This command will remove the player "ironstove." from the pool. This is a strict command. No typos or abbreviations allowed.

	Features:
The bot will assign the creator of the thread as the OP/host. If you want to change this, go into config.txt after the bot has initialized to change the host to whomever you please.You want to do this in the case that someone who is not the host created the thread, OR you want to pass on host privileges to another player to moderate the game by adding/removing players in the pool for day/night actions.

Automatically counts votes, indexes all of the thread information into config.txt. If you want the bot to make certain modifications (Add/remove players, change votes, etc), go into config.txt to edit it in directly (Less clutter) or enter the commands in a post on the thread itself.

The bot will take the playercount to determine hammer and automatically post when hammer is reached and shut itself down.

==================================================
============     REMEMBER THIS     ===============
==================================================
-Use the "KILL" command to remove players after they have been lynched or night killed then run the "DAY BEGINS" command after (Can be done in the same post). If you forget to do this, the bot will possibly make errors when counting votes and definitely miscalculate hammer (It will continue running after hammer is hit depending on the player count)... 

-Treat each command as separate [b] tags. Don't try to combine commands into a single tag, it will screw things up (Applies to both players and the host).

Example of trying to combine and fucking things up:
[b]KILL PLAYER1
KILL PLAYER2
KILL PLAYER3
DAY BEGINS[/b]

Example of not combining and doing it the right way:
[b]KILL PLAYER1[/b]
[b]KILL PLAYER2[/b]
[b]KILL PLAYER3[/b]
[b]DAY BEGINS[/b]