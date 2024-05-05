import tls_client
import time
import datetime
import os, random
import concurrent.futures

red = '\x1b[31m(-)\x1b[0m'
blue = '\x1b[34m(+)\x1b[0m'
green = '\x1b[32m(+)\x1b[0m'
yellow = '\x1b[33m(!)\x1b[0m'

def get_timestamp():
    time_idk = datetime.datetime.now().strftime('%H:%M:%S')
    timestamp = f'[\x1b[90m{time_idk}\x1b[0m]'
    return timestamp

class DiscordSession:
    def __init__(self, client_identifier="chrome112"):
        self.session = tls_client.Session(client_identifier=client_identifier, random_tls_extension_order=True)

    def post(self, url, json_data, headers):
        return self.session.post(url, json=json_data, headers=headers)
    
class SoundboardNuker:
    default_sounds = [
        {'name': 'quack', 'sound_id': '1', 'volume': 1, 'emoji_id': None, 'emoji_name': '🦆', 'user_id': '643945264868098049'},
        {'name': 'airhorn', 'sound_id': '2', 'volume': 1, 'emoji_id': None, 'emoji_name': '🔊', 'user_id': '643945264868098049'},
        {'name': 'cricket', 'sound_id': '3', 'volume': 1, 'emoji_id': None, 'emoji_name': '🦗', 'user_id': '643945264868098049'},
        {'name': 'golf clap', 'sound_id': '4', 'volume': 1, 'emoji_id': None, 'emoji_name': '👏', 'user_id': '643945264868098049'},
        {'name': 'sad horn', 'sound_id': '5', 'volume': 1, 'emoji_id': None, 'emoji_name': '🎺', 'user_id': '643945264868098049'},
        {'name': 'ba dum tss', 'sound_id': '7', 'volume': 1, 'emoji_id': None, 'emoji_name': '🥁', 'user_id': '643945264868098049'}
    ]

    def __init__(self, discord_session, channel_id, token):
        self.discord_session = discord_session
        self.url = f'https://discord.com/api/v9/channels/{channel_id}/send-soundboard-sound'
        self.token = token
        self.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US',
            'content-type': 'application/json',
            'authorization': token,
            'origin': 'https://discord.com',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9037 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Asia/Calcutta',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDM3Iiwib3NfdmVyc2lvbiI6IjEwLjAuMjI2MzEiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMzcgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyODA3MDAsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjQ1MzY5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        }

        self.sound_id = None
        self.emoji_name = None

    def open_lootbox(self):
        selected_item = random.choice(self.default_sounds)
        self.sound_id = selected_item['sound_id']
        self.emoji_name = selected_item['emoji_name']
        json_data = {
            'sound_id': self.sound_id,
            'emoji_id': None,
            'emoji_name': self.emoji_name,
        }
        response = self.discord_session.post(self.url, json_data, headers=self.headers)

        if response.status_code == 403:
            print(f"{get_timestamp()} {yellow} You Are Not In The Voice Channel !")
            time.sleep(2)
        elif response.status_code == 204:
            print(f"{get_timestamp()} {green} Successfully Played A Random Sound.")
        else:
            print(f'{get_timestamp()} {red} An Error Occurred : {response.status_code} - {response.text}')

def main():
    token = input(f"{get_timestamp()} {blue} Please Enter Your Account Token : ")
    channel_id = input(f"{get_timestamp()} {blue} Please Enter The Voice Channel Id : ")
    threads = int(input(f"{get_timestamp()} {blue} Please Enter The Number Of Threads : "))
    discord_session = DiscordSession()
    soundboard_nuker = SoundboardNuker(discord_session, channel_id, token)
    
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(lambda _: soundboard_nuker.open_lootbox(), range(threads))

if __name__ == "__main__":
    os.system("cls")
    main()