# Track player name changes

## Overview

Because the tracker is so tightly integrated with Discord and the RuneScape clan system, it is very important that player names be up-to-date as much as possible. To reliably track a player, their RuneScape display name, discord nickname, and also the name assigned to their record in the tracker spreadsheet must be kept identical at all times.

To that end, it is possible to update a player's records as and when their name changes. Given that a player's RuneScape display name is identical to their discord nickname, the `rename` command can be used to update all relevant records at the same time,

## Syntax

A typical `rename` command is generally structured as follows:

```text
!track rename "<old_name>" "<new_name>" <date>
```

## Arguments {#arguments}

#### old\_name {#player_name}

_Required._ The player's previous name. Always surrounded by double quotes. Case matters, `"JOHN DOE"` and `"john doe"` are considered two different players.

#### new\_name {#player_name}

_Required._ The player's current, updated name. Always surrounded by double quotes. Case matters, `"JOHN DOE"` and `"john doe"` are considered two different players.

#### date {#date}

_Required._ The date the player's name was changed. Specified in the format `M/D/YYYY`. For instance, if the player changed their name on 12 March 1969, `date` would be `3/12/1969`.  


