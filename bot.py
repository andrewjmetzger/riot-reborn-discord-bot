import json
import logging
import random

import discord
from discord.ext import commands

import player
import sheets

Player = player.Player

logging.basicConfig(level=20, format='%(asctime)s - %(levelname)s - %(message)s')

credentials_cfg = json.load(open("./config/credentials.json"))
server_cfg = json.load(open("./config/server.json"))

discord_token = credentials_cfg["discord_token"]

prefix = server_cfg["prefix"]
if len(prefix) > 2:
    prefix += " "
    logging.debug("Prefix is a string, appended space")

logging.warning("prefix == `" + prefix + "`")

bot = commands.Bot(command_prefix=prefix)

bot_channel = None
general_channel = None
greeting_channel = None
info_channel = None

clan_name = server_cfg["clan_name"]

points_per_recruit = server_cfg["points_per_recruit"]
points_per_cap = server_cfg["points_per_cap"]
points_per_attended = server_cfg["points_per_attended"]
points_per_hosted = server_cfg["points_per_hosted"]


@bot.event
async def on_ready():
    logging.debug("--------")
    logging.debug("Starting up...")
    logging.debug(str("Logged in as {0.user}, with ID {0.user.id}".format(bot)))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=prefix + 'rtfm'))

    logging.info(discord.version_info)

    global bot_channel
    global general_channel
    global greeting_channel
    global info_channel

    bot_channel = bot.get_channel(server_cfg["bot_channel"])
    general_channel = bot.get_channel(server_cfg["general_channel"])
    greeting_channel = bot.get_channel(server_cfg["greeting_channel"])
    info_channel = bot.get_channel(server_cfg["info_channel"])

    logging.info("--------")

    doc = sheets.get_sheet()
    sheet = sheets.get_player_sheet()

    logging.info("Opened doc: " + str(doc.title))
    logging.info("Selected sheet: " + str(sheet.title))
    logging.info("Number of rows: " + str(sheet.row_count - 1))

    logging.info("--------")

    bot.remove_command('help')


########################
# CUSTOM JOIN MESSAGES #
########################

member = discord.guild.Member


@bot.event
async def on_member_join(self, member):
    if server_cfg["automatic_greeting"] == "True":
        # Define a list of greetings

        greetings = ["Hey there, {0}".format(str(member.mention)),
                     "Yo, {0}!^".format(str(member.mention)),
                     "Look, someone's here! ... Never mind, it's only "
                     "{0}".format(str(member.mention)),
                     "Really? {0} again?".format(str(member.mention)),
                     "{0} just joined. Everyone, look busy!".format(
                         str(member.mention)),
                     "{0} just joined. Can I get a heal?".format(
                         str(member.mention)),
                     "{0} joined your party.".format(str(member.mention)),
                     "{0} joined. You must construct additional pylons.".format(
                         str(member.mention)),
                     "Ermagherd. {0} is here.".format(str(member.mention)),
                     "Welcome, {0}. Stay awhile and listen.".format(
                         str(member.mention)),
                     "Welcome, {0}. We were expecting you ( ͡° ͜ʖ ͡°)".format(
                         str(member.mention)),
                     "Welcome, {0}. We hope you brought pizza.".format(
                         str(member.mention)),
                     "Welcome {0}. Leave your weapons by the door.".format(
                         str(member.mention)),
                     "A wild {0} appeared.".format(str(member.mention)),
                     "Swoooosh. {0} has landed.".format(str(member.mention)),
                     "Brace yourselves. {0} just joined the server.".format(
                         str(member.mention)),
                     "{0} just arrived. Hide your bananas.".format(
                         str(member.mention)),
                     "{0} just arrived. Seems OP - please nerf.".format(
                         str(member.mention)),
                     "{0} just slid into the server.".format(
                         str(member.mention)),
                     "A {0} has spawned in the server.".format(member.mention),
                     "{0} hopped into the server. Kangaroo!!".format(
                         str(member.mention)),
                     "{0} just showed up. Hold my beer.".format(
                         str(member.mention))]

        msg = random.choice(greetings)

        if server_cfg["info_channel"] != 0:
            msg += "\n If you haven't already, please read everything posted in "
            msg += bot.get_channel(server_cfg["info_channel"]).mention + ", "
            msg += "and then follow the instructions to change your " \
                   "server nickname."

        await greeting_channel.send(msg)

    # TODO: Logic to add evolved role if member is in clan


#################
# DOCUMENTATION #
#################

@bot.group(pass_context=True)
async def rtfm(ctx):
    """
    Show detailed help information.

    Usage:
        !track rtfm
    """

    msg = "For more detailed help and usage "
    msg += "information please see the "
    msg += "latest documentation online: \n" \
           "<https://docs.mtz.gr/clan-tracker-discord-bot/>"

    await bot_channel.send(msg)


################
# BOT COMMANDS #
################

@bot.group(pass_context=True)
async def track(ctx):
    """
    The base command. Does nothing on its own
    Usage:
        !track <subcommand> "[player_name]" [date]

    See also: '!track rtfm' for more information.
    """

    if ctx.invoked_subcommand is None:
        msg = "[ERR] Nothing interesting happens. (Unknown or bad command)\n"
        msg += "*Check your message for errors and try again."
        msg += "Perhaps you should*"
        msg += "`!track rtfm`*?*"
        await bot_channel.send(msg)


@bot.command(pass_context=True)
async def joined(ctx, player_name: str, date: str, recruited_by=None):
    """
        Add a player to the clan tracker. Optionally, track who recruited them.

    Usage:
        !track joined "<player_name>" <date> "[recruited_by]"
    """

    Player.new(player_name, date, recruited_by=None)

    msg = "Awww yeah! __" + player_name + "__ finally joined " + clan_name + " "
    msg += "on " + date + ".  "

    if recruited_by is not None:
        player = Player.find(player_name)
        player.recruited_by = recruited_by
        recruiter = Player.find(recruited_by)
        recruiter.total_points += points_per_recruit
        msg += "__" + recruited_by + "__ earned " + str(
            points_per_recruit) + " point(s) for recruiting them.\n"

    else:
        player = Player.find(player_name)
        player.recruited_by = ""
        msg += ""

    await bot_channel.send(msg)


@bot.command(pass_context=True)
async def leave(ctx, player_name: str):
    """
    Remove a player from the tracker.

    Usage:
        !track leave "<player_name>"

    This command should be used sparingly -- it is a destructive action.
    """

    import time
    await ctx.trigger_typing()

    Player.find(player_name).delete()

    msg = ""
    msg += "[WARN] The record for __" + player_name + "__ was removed "
    msg += "by " + str(ctx.message.author.name) + " "
    msg += "on " + time.strftime("%Y-%m-%d") + ".\n"
    msg += "*If this was not intended, notify your administrator immediately "
    msg += "so that they can try to revert the change.*"

    await bot_channel.send(msg)


@bot.command(pass_context=True)
async def capped(ctx, player_name: str, date: str):
    """
    Increases Times Capped by 1.

    Usage:
        !track capped "<player_name>" <date>
    """

    ctx.trigger_typing()

    player = Player.find(player_name)
    player.times_capped += 1
    player.total_points += points_per_cap
    player.last_cap = date

    msg = "Woohoo! __" + player_name + "__ has capped on " + date + "! "
    msg += "They just earned " + str(points_per_cap) + " point(s). \n"
    msg += "*(More info: `!track whois \"" + player_name + "\"`)*"

    await bot_channel.send(msg)


@bot.command(pass_context=True)
async def attended(ctx, player_name: str, date: str):
    """
    Registers attendance at an event.

    Usage:
        !track attended "<player_name>" <date>
    """

    ctx.trigger_typing()

    player = Player.find(player_name)
    player.events_attended += 1
    player.total_points += points_per_attended
    player.last_event = date

    msg = "Alright! __" + player_name + "__ earned "
    msg += str(points_per_attended) + " point(s) "
    msg += "for attending an event on " + date + ".\n"
    msg += "*(More info: `!track whois \"" + player_name + "\"`)*"
    await bot_channel.send(msg)


@bot.command(pass_context=True)
async def hosted(ctx, player_name: str, date: str):
    """
    Registers a hosted event.

    Usage:
        !track hosted "<player_name>" <date>
    """

    ctx.trigger_typing()

    player = Player.find(player_name)
    player.events_hosted += 1
    player.total_points += points_per_hosted
    player.last_event = date

    msg = "Alright! __" + player_name + "__ earned " + str(
        points_per_hosted) + " point(s) "
    msg += "for hosting an event on " + date + ".\n"
    msg += "*(More info: `!track whois \"" + player_name + "\"`)*"
    await bot_channel.send(msg)


@bot.command(pass_context=True)
async def whois(ctx, player_name: str):
    """
    Get information about a specified player.

    Usage:
        !track whois "<player_name>"
    """

    await ctx.trigger_typing()

    info = "```\n"
    info += "**RECORDS FOR " + player_name.upper() + "**\n"
    info += ('-' * (len(info) - 5)) + "\n"

    player = Player.find(player_name)

    info += "      Player Name : \"" + player.name + "\"\n"
    info += "        Join Date : " + player.join_date + "\n"
    info += "     Recruited By : \"" + player.recruited_by + "\"\n"
    info += "             Rank : " + player.rank + "\n"
    info += "  Events Attended : " + str(int(player.events_attended)) + " "
    info += "(" + str(points_per_attended) + " point(s) each) \n"
    info += "    Events Hosted : " + str(int(player.events_hosted)) + " "
    info += "(" + str(points_per_hosted) + " point(s) each) \n"
    info += "      (Last Event : " + player.last_event + ")\n"
    info += "     Times Capped : " + str(int(player.times_capped)) + " "
    info += "(" + str(points_per_cap) + " point(s) each) \n"
    info += "        (Last Cap : " + player.last_cap + ")\n"
    info += "Players Recruited : " + str(int(player.players_recruited)) + " "
    info += "(" + str(points_per_recruit) + " point(s) each) \n"
    info += "     Total Points : " + str(player.total_points) + "\n"
    info += "```"

    await ctx.send(info)


@bot.command(pass_context=True)
async def rename(ctx, old_name: str, new_name: str, date: str):
    """
    Rename a player when they change their in-game name. Also changes their
    discord nickname, if linked.

    Usage:
        !track rename "<old_name>" "<new_name>" <date>
    """
    await ctx.trigger_typing()

    Player.name = new_name
    # TODO: Also change discord nickname

    msg = '"__' + old_name + '__" was renamed to "__' + new_name
    msg += '__" by ' + str(ctx.message.author.nick) + ' on ' + date + '.\n'
    msg += "[WARN] *Please use the new name when referencing this player"
    msg += " in the future, or the bot will get confused.*"

    await bot_channel.send(msg)


@bot.command(pass_context=True)
async def dm(ctx, recipient, msg):

    recipient = bot.get_user(ctx.message.mentions[0].id)
    print(recipient)

    msg = msg.replace("$nick", str(recipient))
    await recipient.send(msg)


################################
#        UTILS COMMANDS        #
################################

@bot.group(pass_context=True, hidden=True)
async def utils():
    """
    Here be dragons. USE ONLY AS DIRECTED!

    Usage:
    !track utils <utility> [parameters]
        Hey, stop that!. These are dangerous.
    """


@utils.command(pass_context=True)
async def more(ctx):
    msg = "[ERR] Invalid command. \n"

    await bot_channel.send(msg)


@utils.command(pass_context=True)
async def suspend(ctx, duration: int = 15):
    msg = "\n<@here>\n\n"
    msg += "**NOTICE:**  "
    msg += "The tracker system will be going offline "
    msg += "for maintenance momentarily. "
    msg += "While the bot is offline, "
    msg += "all commands will be ignored. "
    msg += "Functionality should be restored "
    msg += "at the end of the maintenance "
    msg += "window. "
    msg += "Estimated downtime is currently "
    msg += "__" + str(duration) + " minutes__.\n\n"
    msg += "Notifications will be sent when "
    msg += "maintenance has "
    msg += "concluded. "
    msg += "To make updates while the bot is offline, DM an administrator. "
    msg += "Thank you for your "
    msg += "patience while we work to restore "
    msg += "functionality "
    msg += "as soon as possible."

    await bot_channel.send(msg)

    await bot.logout()


@utils.command(pass_context=True)
async def resume(ctx):
    msg = "\n<@here>\n\n"
    msg += "**NOTICE:**  "
    msg += "The tracker system is now online. "
    msg += "Thank you for your patience."

    await bot_channel.send(msg)


if __name__ == '__main__':
    bot.run(discord_token)
