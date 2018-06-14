# Track events hosted

## Overview

You can record when a player hosts a clan event with the `hosted` command. This increases the player's _Events Hosted_ by one, and adds the appropriate number of points to the player's total.

## Syntax

A typical`hosted` command is generally structured as follows:

```text
!track hosted "<player_name>" <date>
```

## Arguments

#### player\_name

_Required._ The name of the player who hosted the event. Always surrounded by double quotes. Case matters, `"JOHN DOE"` and `"john doe"` are considered two different players.

#### date

_Required._ The date `player_name`  hosted the event. Specified in the format `M/D/YYYY`. For instance, if a player hosted an event on 12 March 1969, `date` would be `3/12/1969`.

