import asyncio
from pyrogram import *
from pyrogram.handlers import *
from pyrogram.types import *
from pyrogram.errors import *
import requests

OWNER_API_KEY = "OWNER_API_KEY"
OWNER_ID = "OWNER_ID"
API_ID = "API_ID"
API_HASH = "API_HASH"
BOT_TOKEN = "BOT_TOKEN"
ADMIN_API_KEY = "ADMIN_API_KEY"
API_URL = "telegram.starkai.live"

app = Client(name='STARK-API',api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)


@app.on_message(filters.command(["start","help"]))
async def start(_, message: Message):
  return await message.reply("Welcome to Stark AntiSpam System!\n\nCommands!\n/start - Start The Bot\n/status - To get your Information\n/admins - To Get the list of Admins\n/get_api - To generate API KEY (Admins)\n/check_api - Show your API KEY (Admins)\n/ban - To Ban any user! (Admins)\n/unban - To Unban any user! (Admins)\n/get_trust - To get the Users Trust Score\n/check - To check the status of the User\n/add_admin - To add Admins (Owner)\n/rm_admin - To remove Admins (owner)")
  
  
@app.on_message(filters.command("add_admin"))
async def add_admin(_, message: Message):
      if message.from_user.id == OWNER_ID:
        pass
      else:
        return await message.reply("Not an Authorized User!")
      
      if message.reply_to_message:
        reply = message.reply_to_message
        user_id = reply.from_user.id
      else:
        return await message.reply("Tag any user to make Admin!")
        
      data = requests.get(f"https://{API_URL}/addsudo?user_id={user_id}&api_key={OWNER_API_KEY}")
      r = data.json()
      msg = r["message"]
      return await message.reply(msg)

@app.on_message(filters.command("rm_admin"))
async def rm_admin(_, message: Message):
      if message.from_user.id == OWNER_ID:
        pass
      else:
        return await message.reply("Not an Authorized User!")
      if message.reply_to_message:
        reply = message.reply_to_message
        user_id = reply.from_user.id
      else:
        return await message.reply("Tag Admin to Remove!")
        
      data = requests.get(f"https://{API_URL}/rmsudo?user_id={user_id}&api_key={OWNER_API_KEY}")
      r = data.json()
      msg = r["message"]
      return await message.reply(msg)

@app.on_message(filters.command("get_api") & filters.private)
async def get_api(_, message: Message):
  user_id = message.from_user.id
  data = requests.get(f"https://{API_URL}/get_api_key?user_id={user_id}")
  r = data.json()
  msg = r["message"]
  return await message.reply(msg)


@app.on_message(filters.command("check"))
async def check(_, message: Message):
  user_id = message.from_user.id
  data = requests.get(f"https://{API_URL}/check?user_id={user_id}")
  if data.status_code == 201:
    return await message.reply("You are Not Banned!")
  else:
    r = data.json()
    userid = r['user_id']
    admin = r['admin']
    reason = r['banned_reason']
    time = r['banned_time']
    await message.reply(f"**Your Banned!**\n\nYour ID: `{userid}`\nBanned By: `{admin}`\nReason: `{reason}`\nTime: `{time}`")

@app.on_message(filters.command("get_trust"))
async def get_trust(_, message: Message):
  if message.reply_to_message:
    reply = message.reply_to_message
    user_id = reply.from_user.id
  else:
    user_id = message.from_user.id
    
  data = requests.get(f"https://{API_URL}/gettrust?user_id={user_id}")
  if data.status_code == 404:
    return await message.reply("Data Not Found or User Maybe System Admin")
  else:
    r = data.json()
    userid = r['user_id']
    spamscore = r['spam_avg'] * 100
    return await message.reply(f"**Data Found!**\n\nUser ID: `{userid}`\nSpam Score: `{spamscore} %`")

@app.on_message(filters.command("status"))
async def status(_, message: Message):
    if message.reply_to_message:
        reply = message.reply_to_message
        user_id = reply.from_user.id
    else:
        user_id = message.from_user.id
        
    data = requests.get(f"https://{API_URL}/check_user?user_id={user_id}")
    r = data.json()
    is_admin = r['is_admin']       
    spam_score = r['spam_score']
    is_banned = r['is_banned']
    msg = f"User ID: `{user_id}`\nAdmin Status: `{is_admin}`\nIs Banned: `{is_banned}`\nSpam Score: `{spam_score} %`"
    if is_banned == "True":
      admin = r['admin']
      reason = r['banned_reason']
      time = r['banned_time']
      msg += f"\nReason: `{reason}`\nAdmin: `{admin}`\nTime: `{time}`"

    return await message.reply(msg)
  
@app.on_message(filters.command("admins"))
async def admins(_, message: Message):
  data = requests.get(f"https://{API_URL}/admins")
  r = data.json()
  admins = r['message']
  return await message.reply(admins)

@app.on_message(filters.command("ban"))
async def ban(_, message: Message):
      if len(message.command) < 2:
         return await message.reply("Reason Not Provided")

      reason = message.text.split(None, 1)[1]
      if message.reply_to_message:
        reply = message.reply_to_message
        user_id = reply.from_user.id
      else:
        return await message.reply("Tag any user to Ban")
        
      data = requests.get(f"https://{API_URL}/ban_user?user_id={user_id}&api_key={ADMIN_API_KEY}&reason={reason}")
      r = data.json()
      msg = r["message"]
      return await message.reply(msg)
  
@app.on_message(filters.command("unban"))
async def unban(_, message: Message):
      reason = message.text
      if message.reply_to_message:
        reply = message.reply_to_message
        user_id = reply.from_user.id
      else:
        return await message.reply("Tag any user to Unban")
        
      data = requests.get(f"https://{API_URL}/unban_user?user_id={user_id}&api_key={ADMIN_API_KEY}")
      r = data.json()
      msg = r["message"]
      return await message.reply(msg)

@app.on_message(filters.incoming)
async def check_message(client, message):
  msg = message.text
  chat_id = message.chat.id
  user_id = message.from_user.id
  data = requests.get(f"https://{API_URL}/check_message?user_id={user_id}&message={msg}")
  ban = requests.get(f"https://{API_URL}/check_user?user_id={user_id}")
  if data.status_code == 200:
    return
  else:
    print("System UnRecognised")
   
  rb = ban.json()
  is_ban = rb['is_banned']
  if is_ban == "True":
    try:
      await app.ban_chat_member(chat_id, user_id)
      reason = rb['banned_reason']
      admin = rb['admin']
      time = rb['banned_time']
      spam_score = rb['spam_score'] * 100
      TEXT = f"User was banned in Stark AntiSpam System!\n\nUser ID: `{user_id}`\nReason: `{reason}`\nAdmin: `{admin}`\nSpam Score: `{spam_score} %`\nTime: `{time}`"
      return await app.send_message(chat_id=chat_id,text=TEXT)
    except Exception as e:
      reason = rb['banned_reason']
      admin = rb['admin']
      time = rb['banned_time']
      spam_score = rb['spam_score'] * 100
      TEXT = f"User was banned in Stark AntiSpam System!\n\nUser ID: `{user_id}`\nReason: `{reason}`\nAdmin: `{admin}`\nSpam Score: `{spam_score} %`\nTime: `{time}`"
      return await message.reply(TEXT)
      
    

    
        
def main():
  try:
    app.run()
    print("Started Successfully")
  except FloodWait as e:
    print(f"Sleeping for {e.value} seconds!")


if __name__ == "__main__":
                   main()
                   
