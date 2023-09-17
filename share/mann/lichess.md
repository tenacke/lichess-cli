% lichess(1) 0.1.0
% Emre Kılıç <emrekilic1010@gmail.com>
% 2023-09-14

# NAME
lichess - lichess command line interface

# SYNOPSIS
lichess <command> [<args>]

# DESCRIPTION
Lichess is an open source chess server. This is a command line interface through Lichess API. 
You can run different commands to use Lichess API and configure your settings and tokens.

# COMMANDS
You can run `lichess help <command>` to see the manual for a command.

General
    token <command> [<args>]             Manage lichess API tokens
    config <command> [<args>]            Edit configuration details
    account <command> [<args>]           Manage lichess account
    relations <command> [<args>]         Control lichess community relations
    user <command> [<args>]              Get lichess user info
    team <command> [<args>]              Make lichess team operations

Game
    game <command> [<args>]              See and add lichess games
    puzzle <command> [<args>]            Play lichess puzzles
    study <command> [<args>]             Read lichess studies
    board <command> [<args>]             Play lichess through board API
    simuls <command> [<args>]            Play lichess simuls
    challenge <command> [<args>]         Challenge lichess players
    tournament <command> [<args>]        Participate lichess tournaments
    bulk <command> [<args>]              Bulk operations on lichess games

Miscellaneous
    bot <command> [<args>]               Use bot accounts
    tablebase <command> [<args>]         Query lichess tablebases
    explorer <command> [<args>]          Explore lichess games
    broadcast <command> [<args>]         Send and receive lichess broadcast messages
    message <command> [<args>]           Send lichess messages
    tv <command> [<args>]                Watch lichess TV
    help <command>                       Show manual for a command

# SEE ALSO
https://lichess.org/api

# AUTHOR
Emre Kılıç <emrekilic1010@gmail.com>

# LICENSE
This project is licensed under WTFPL. You can do what the fuck you want to do. See LICENSE file for details.
