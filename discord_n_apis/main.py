import asyncio
import requests
import discord
from pdb import set_trace as bp
import os
from discord.message import Message
from db import DB
import json
from ctfd import register_user
from twilio.rest import Client
import logging

# from dotenv import load_dotenv
# load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logger.info('App Started')

intents = discord.Intents.default()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

twi_client = Client(account_sid, auth_token)

client = discord.Client(intents=intents)
ongoing_verifications = dict()

# First create/load db
users_db = DB('users_db.json')
form_registered_users = json.load(open('users.json'))
for user in form_registered_users.values():
    if users_db.search('email', user['Email ID']):
        continue
    # Add entry in db
    users_db.data.append({
        'name': user['Name'],
        'email': user['Email ID'],
        'phone_num': user['Phone Number'],
    })
users_db.save()
print('DB loaded')


async def check_leaderboard(message):
    while True:
        embed = discord.Embed(title="Leaderboard", color=discord.Color.gold())
        r = requests.get("https://ctf.devclub.in/api/v1/scoreboard")
        headers = {
            'Authorization': f"Token {os.getenv('CTFD_ACCESS_TOKEN')}",
            'Content-Type': 'application/json',
        }
        r = requests.get("https://ctf.devclub.in/api/v1/scoreboard")
        data = r.json()
        print(data)
        for user in sorted(data["data"], key=lambda x: int(x['pos'])):
            rank = str(user["pos"])
            if int(user["pos"]) > 7:
                continue
            name = user["name"]
            points = str(user["score"])
            embed.add_field(name=f"`#{rank}`: {name}",
                            value=f"Points: `{points}`", inline=False)
        await message.edit(content=None, embed=embed)
        await asyncio.sleep(60)


async def check_updates(channel, last, log):
    while True:
        # r = requests.get("https://ctf.devclub.in/api/updates")
        headers = {
            'Authorization': f"Token {os.getenv('CTFD_ACCESS_TOKEN')}",
            'Content-Type': 'application/json',
        }

        r = requests.get(
            'http://localhost:4000/api/v1/submissions', headers=headers)
        data = r.json()['data']

        for u in data["updates"]:
            _id = u["_id"]
            if _id <= last:
                continue
            time = u["time"]
            category = u["category"]
            msg = u["message"]
            embed = discord.Embed(title=msg, color=discord.Color.red())
            embed.add_field(name="Time", value=time, inline=True)
            embed.add_field(name="Category", value=category, inline=True)
            await channel.send(embed=embed)
            await log.send(f"Posted update with id {_id}")
            last = _id
        await asyncio.sleep(30)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    # bp()
    if message.author == client.user:
        return
    channel = message.channel

    if message.content.lower().startswith("?leaderboard"):
        if discord.utils.get(message.guild.roles, name="Admin") in message.author.roles:
            for c in message.raw_channel_mentions:
                try:
                    channel = message.guild.get_channel(c)
                    msg = await channel.send("Leaderboard")
                    await check_leaderboard(msg)
                except:
                    await message.reply(f"Cannot track leaderboard")
        else:
            await message.reply("Only admins can use this command")

    if message.content.lower().startswith("?sendupdate"):
        if discord.utils.get(message.guild.roles, name="Admin") in message.author.roles:
            for c in message.raw_channel_mentions:
                try:
                    channel = message.guild.get_channel(c)
                    cmd = message.content.split(";")
                    msg = cmd[1]
                    time = cmd[2]
                    category = cmd[3]

                    embed = discord.Embed(title=msg, color=discord.Color.red())
                    embed.add_field(name="Time", value=time, inline=True)
                    embed.add_field(name="Category",
                                    value=category, inline=True)
                    await channel.send(embed=embed)
                except:
                    await message.reply(f"Cannot send updates. Format is ?sendupdate ;<msg>;<time>;<cat>; #channel")
        else:
            await message.reply("Only admins can use this command")

    if message.content.lower().startswith("?updates"):
        if discord.utils.get(message.guild.roles, name="Admin") in message.author.roles:
            for c in message.raw_channel_mentions:
                try:
                    channel = message.guild.get_channel(c)
                    last = int(message.content.split()[1])
                    await check_updates(channel, last, message.channel)
                except:
                    await message.reply(f"Cannot track updates")
        else:
            await message.reply("Only admins can use this command")

    if (isinstance(message.channel, discord.channel.DMChannel)):

        if message.author.id in ongoing_verifications and ongoing_verifications[message.author.id] != 0:
            # user should have entered OTP
            if message.content.strip().find(' ') != -1:
                await message.reply("Please enter valid OTP.")
                ongoing_verifications[message.author.id][0] = 0
                return
            # check if OTP is correct
            email = ongoing_verifications[message.author.id][1]
            users = users_db.search('email', email)
            verification = twi_client.verify.services(os.getenv('twilio_service_key')).verification_checks.create(
                to=f'+91{users[0]["phone_num"]}', code=message.content)
            if verification.status == 'approved':
                # OTP is correct
                await message.reply(embed=discord.Embed(title="Phone Verification Successfull :partying_face: Please wait while we activate your account at CTFd", color=discord.Color.gold()))
                # Now create an account in CTFd
                try:
                    password = register_user(users[0])
                    embed = discord.Embed(
                        title="Account activated successfully", color=discord.Color.blue())
                    embed.add_field(name="CTFd email",
                                    value=email, inline=False)
                    embed.add_field(name="CTFd password",
                                    value=password, inline=False)
                    await message.reply(embed=embed)

                    ongoing_verifications[message.author.id] = 0
                    users[0]['password'] = password
                    users[0]['phoneVerified'] = True
                    users[0]['discordVerified'] = True
                    users[0]['id'] = message.author.id
                    users[0]['discordId'] = message.author.name

                    users_db.save()
                except Exception as e:
                    print('Error in CTFD Registration', e)
                    ongoing_verifications[message.author.id] = 0
                    await message.reply("Error in registering user in CTFd. Please try again(including phone verification) or else contact one of the organizers if the problem persists.")
                    return
                guild = client.get_guild(969586781542563880)
                member = await guild.fetch_member(message.author.id)
                await member.add_roles(discord.utils.get(guild.roles, name="Verified"))
                try:
                    await member.edit(nick=users[0]['name'])
                except:
                    await message.reply("Couldn't change nick")
                await message.reply(f"Congrats! Your account is now active at CTFd :tada: Visit https://ctf.devclub.in and login with the credentials sent to your email.\n Enjoy Hacking!!!")
                return
            else:
                ongoing_verifications[message.author.id][0] += 1
                await message.reply("Incorrect OTP. Please enter the correct OTP")
                if ongoing_verifications[message.author.id][0] >= 5:
                    await message.reply("You have entered wrong OTP too many times. Please try again in one hour.")
                    ongoing_verifications[message.author.id] = 0
            return
        # Check if it is a verification mail
        message_text = message.content.lower()
        if message_text.startswith("verify "):
            # Check if the user is in the db
            email = message_text.split(' ')[1]
            # bp()
            users = users_db.search('email', email)
            if(len(users) == 0):
                await message.reply("User entry not found. Please try again, or contact one of the organizers incase the problem persists.")
                return

            # Check if the user is already verified
            try:
                if(users[0]['phoneVerified']):
                    await message.reply("User Discord Already Verified.")
                    return
            except:
                ...
            embed = discord.Embed(
                title="Hi " + users[0]['name'], color=discord.Color.green())
            embed.add_field(name="Please enter the verification code sent to your phone number",
                            value=users[0]['phone_num'], inline=False)
            await message.reply(embed=embed)
            # Verify the user
            ongoing_verifications[message.author.id] = [1, users[0]['email']]
            verification = twi_client.verify.services(os.getenv('twilio_service_key')).verifications.create(to=f'+91{users[0]["phone_num"]}', channel='sms')
            return
    elif message.content.lower().startswith('verify'):
        await message.reply("Please use this bot in DM only.")
        await message.author.send('Hello. Please Run `verify <email>` to verify your account.')
        try:
            await message.delete()
        except:
            ...
bot_token = os.getenv('DISCORD_TOKEN')
print(bot_token)
client.run(bot_token)
