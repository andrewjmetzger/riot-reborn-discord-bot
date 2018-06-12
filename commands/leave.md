# Track players leaving

## Overview {#overview}

You can record when a player leaves the clan with the `leave` command. This removes the player's record from the spreadsheet, which prevents them from being tracked in the future.

{% hint style="danger" %}
The `leave` command is highly destructive, and in most cases, _permanent_. Although administrators have the ability to override most of the bot's actions, this is not always the case. Do not rely on such powers, _your administrators may not be able to revert the deletion_.

**Use this function sparingly**. You have been warned.
{% endhint %}

## Syntax {#syntax}

A typical`leave` command is generally structured as follows:

```text
!track leave "<player_name>" <date>
```

## Arguments {#arguments}

#### player\_name {#player_name}

_Required._ The name of a player who left the clan. Always surrounded by double quotes.

#### date {#date}

_Required._ The date `player_name` left the clan. Specified in the format `M/D/YYYY`. For instance, if the player left on 12 March 1969, `date` would be `3/12/1969`.  


## Recover recently deleted records

For information on restoring recently deleted records, see the help topic linked below.

{% page-ref page="../troubleshooting/recover-deleted-records.md" %}



