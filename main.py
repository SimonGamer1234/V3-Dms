import requests
import json
import time
import os
# Replace with your own Discord API URL, or use the global one (https://discord.com/api/)
DISCORD_API_BASE_URL = "https://discord.com/api/v9"

Tokens_data = json.load(os.getenv("ACCOUNTS").strip())

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN").strip()


file = "Account_Messages.json"

with open(file, "r") as f:
    read_messages_data = json.load(f)
guild_id = "1302654530474737767"
def get_user_dms(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    # Fetch DMs for the user
    url = f"{DISCORD_API_BASE_URL}/users/@me/channels"
    response = requests.get(url, headers=headers)
    time.sleep(1)
    print(response.status_code)
    
    if response.status_code == 200:
        dm_channels = response.json()
        # print(json.dumps(dm_channels, indent=4))
        
            
    elif response.status_code == 401:
        # Unauthorized (invalid token)
        print("Error: Invalid authentication token.")
    else:
        # Some other error occurred
        print(f"Error: {response.status_code} - {response.text}")

    return dm_channels

def check_unread(dm_channels_data, token, read_messages_data, name):
    for channel in dm_channels_data:
        channel_id = channel["id"]
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
        headers = {
            "Authorization": token,
        }
        response = requests.get(url, headers=headers)
        time.sleep(2)
        data = response.json()
        
        print(json.dumps(data, indent=4))
        last_message_id = channel["last_message_id"]
        index = 1000
        Found = False
        for part in read_messages_data:
            if part["user"] == name:
                user_part = part["read-messages"]

        for read_message in user_part:
            if read_message["channel-id"] == channel_id:
                Found = True
                for message in data:
                    message_id = message["id"]
                    if read_message["last-message-id"] == message_id:
                        index = data.index(message)
                        print("changing index to",index )
                read_message["last-message-id"] = last_message_id
        if Found == False:
            user_part.append({
                "channel-id": channel_id,
                "last-message-id": last_message_id
            })
        messages_to_print = []
        for message in data:
            message_index = data.index(message)
            message_embeds = message["embeds"]
            message_author_id = message["author"]["id"]
            message_author_username = message["author"]["username"]
            
            if message_index < index:
                messages_to_print.append({
                    "content": message["content"],
                    "id": message["id"],
                    "index": message_index,
                    "embeds": message_embeds,
                    "name": message_author_username,
                    'ID': message_author_id,
                    "account": name
                })                 
        messages_to_print.sort(key=lambda m: m["index"], reverse=True)
        for message in messages_to_print:

            CHANNEL_ID = "1387532557863616662"

            url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"

            headers = {
                "Authorization": f"Bot {Discord_BOT_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "content": f"{name}\n-# New message from {message["name"]} | {message["id"]}\n\n{message["content"]}",
                "embeds": message["embeds"]
                
            }

            response = requests.post(url, headers=headers, json=payload)
            time.sleep(1)
            print(response.status_code)
            print(response.text)

        with open(file, "w") as f:
            json.dump(read_messages_data, f, indent=4)


def main():
    for token1 in Tokens_data:
        print(token1)
        token = token1["Token"]
        name = token1["Name"]
        cathegory = token1["Cathegory"]
        if "Test" not in cathegory:
            dm_channels_data = get_user_dms(token)
            check_unread(dm_channels_data, token, read_messages_data, name)

main()