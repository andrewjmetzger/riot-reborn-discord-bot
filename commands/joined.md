# Track new recruits

## Overview

You can add a new recruit to the tracker with the `joined` command. This adds another record to the tracker spreadsheet, setting the relevant fields to their default values.

## Syntax

A typical`joined` command is generally structured as follows:

```text
!track joined "<new_player>" <date> "[recruiter]"
```

## Arguments

#### new\_player

_Required._ The name of the player to add to the tracker. Always surrounded by double quotes.

#### date

_Required._ The date `new_player` was recruited into the clan. Specified in the format `M/D/YYYY`. For instance, if a player was recruited on 12 March 1969, `date` would be `3/12/1969`.

#### recruiter

_Optional_. If points are awarded for new recruits, the name of the existing player who recruited `new_player` into the clan. Always surrounded by double quotes.

Awards the appropriate number of points to the recruiter, if specified. Has no effect otherwise.

