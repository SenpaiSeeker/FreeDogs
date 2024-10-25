import os
import time
import json
import requests
import logging
import hashlib
from datetime import datetime


def print_banner():
    print("""
▄▀█ █ █▀█ █▀▄ █▀█ █▀█ █▀█ ∞
█▀█ █ █▀▄ █▄▀ █▀▄ █▄█ █▀▀   
┏━┓ ┏━┓         ┏━┓ ╔═╗             ╔═╗ ┏━┓__            ┏━┓
┃ ┃ ┃ ┃ ┏━╻━━━┓ ┃ ┃ ┏━┓ ┏━╻━━╻━━━━┓ ┏━┓ ┃ ┏━┛  ┏━━━━╮ ╭━━╹ ┃
┃ ┗━┛ ┃ ┃ ┏━┓ ┃ ┃ ┃ ┃ ┃ ┃ ┏━┓ ┏━┓ ┃ ┃ ┃ ┃ ┗━━┓ ┃ ┏━━┛ ┃ ━━ ┃
┗━━━ ━┛ ┗━┛ ┗━┛ ┗━┛ ┗━┛ ┗━┛ ┗━┛ ┗━┛ ┗━┛ ┗━━━━┛ ┗━━━━┛ ╰━━━━┛
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
               🐶  █▀ █▀█ █▀▀ █▀▀ █▀▄ █▀█ █▀▀ █▀ ▄▄ █▄▄ █▀█ ▀█▀
                   █▀ █▀▄ ██▄ ██▄ █▄▀ █▄█ █▄█ ▄█ ░░ █▄█ █▄█ ░█░  
  """)
    print("==> 🟦 join channel : https://t.me/UNLXairdop")
    print("==> 🟦 join chat : https://t.me/+aXm5TBeS-QMyMGZl")
    print("==================================≠===============")
    print("==> ⬛ github : https://github.com/Rextouin-R/")
    print("====================================≠=============")


# Konfigurasi logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class FreeDogs:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://app.freedogs.bot",
            "Referer": "https://app.freedogs.bot/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }

    def countdown(self, seconds):
        for i in range(seconds, -1, -1):
            print(f"Wait {i} seconds to continue the loop", end='\r')
            time.sleep(1)
        logger.info("")

    def call_api(self, init_data):
        url = f"https://api.freedogs.bot/miniapps/api/user/telegram_auth?invitationCode=oscKOfyL&initData={init_data}"
        try:
            response = requests.post(url, headers=self.headers)
            response_data = response.json()
            if response.status_code == 200 and response_data.get("code") == 0:
                return {"success": True, "data": response_data.get("data")}
            return {"success": False, "error": response_data.get("msg")}
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}

    def is_expired(self, token):
        header, payload, sign = token.split(".")
        decoded_payload = json.loads(base64.urlsafe_b64decode(payload + '==').decode())
        
        try:
            exp_time = decoded_payload.get("exp")
            now = int(datetime.now().timestamp())

            if exp_time:
                expiration_date = datetime.fromtimestamp(exp_time).strftime('%Y-%m-%d %H:%M:%S')
                logger.info(f"Token expires on: {expiration_date}")
                
                is_expired = now > exp_time
                logger.info(f"Has the token expired? {'Yes' if is_expired else 'No'}")
                return is_expired
            else:
                logger.warning("Perpetual token, expiration time cannot be read")
                return False
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return True

    def get_game_info(self, token):
        url = "https://api.freedogs.bot/miniapps/api/user_game_level/GetGameInfo?"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response_data = response.json()
            if response.status_code == 200 and response_data.get("code") == 0:
                data = response_data.get("data")
                logger.info(f"The current balance: {data.get('currentAmount')}")
                logger.info(f"Coin Pool: {data.get('coinPoolLeft')}/{data.get('coinPoolLimit')}")
                logger.info(f"Number of clicks today: {data.get('userToDayNowClick')}/{data.get('userToDayMaxClick')}")
                return {"success": True, "data": data}
            return {"success": False, "error": response_data.get("msg")}
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}

    def md5(self, input):
        return hashlib.md5(input.encode()).hexdigest()

    def collect_coin(self, token, game_info):
        url = "https://api.freedogs.bot/miniapps/api/user_game/collectCoin"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}

        collect_amount = min(game_info["coinPoolLeft"], 10000 - game_info["userToDayNowClick"])
        collect_seq_no = int(game_info["collectSeqNo"])
        hash_code = self.md5(f"{collect_amount}{collect_seq_no}7be2a16a82054ee58398c5edb7ac4a5a")

        params = {
            "collectAmount": collect_amount,
            "hashCode": hash_code,
            "collectSeqNo": collect_seq_no,
        }

        try:
            response = requests.post(url, data=params, headers=headers)
            response_data = response.json()
            if response.status_code == 200 and response_data.get("code") == 0:
                logger.info(f"Successfully collected {collect_amount} coins")
                return {"success": True, "data": response_data.get("data")}
            return {"success": False, "error": response_data.get("msg")}
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}

    def process_tasks(self, token, user_id):
        task_list_result = self.get_task_list(token)
        if task_list_result["success"]:
            for task in task_list_result["data"]:
                logger.info(f"Performing task: {task['name']}")
                complete_result = self.complete_task(token, task["id"])
                if complete_result["success"]:
                    logger.info(f"Completed task {task['name']} successfully | Reward: {task['rewardParty']}")
                else:
                    logger.error(f"Cannot complete task {task['name']}: {complete_result['error']}")
                time.sleep(1)
        else:
            logger.error(f"Unable to get task list for account {user_id}: {task_list_result['error']}")

    def main(self):
        data_file = "data.txt"
        token_file = "token.json"
        
        if os.path.exists(token_file):
            with open(token_file, "r") as file:
                tokens = json.load(file)
        else:
            tokens = {}

        with open(data_file, "r") as file:
            data = [line.strip() for line in file if line.strip()]
        
        while True:
            for i, raw_init_data in enumerate(data):
                user_data = json.loads(raw_init_data)
                user_id = user_data.get("id")
                first_name = user_data.get("first_name")

                logger.info(f"Account {i + 1} | {first_name}")

                token = tokens.get(user_id)
                need_new_token = not token or self.is_expired(token)

                if need_new_token:
                    logger.info(f"Need to get new token for account {user_id}...")
                    api_result = self.call_api(raw_init_data)

                    if api_result["success"]:
                        tokens[user_id] = api_result["data"]["token"]
                        with open(token_file, "w") as file:
                            json.dump(tokens, file, indent=2)
                        logger.info(f"New token has been saved for account {user_id}")
                    else:
                        logger.error(f"Failed to get token for account {user_id}: {api_result['error']}")
                        continue

                game_info_result = self.get_game_info(token)
                if game_info_result["success"]:
                    if game_info_result["data"]["coinPoolLeft"] > 0:
                        self.collect_coin(token, game_info_result["data"])
                    else:
                        logger.warning(f"No coins to collect for account {user_id}")

                    self.process_tasks(token, user_id)
                else:
                    logger.error(f"Unable to get game information for account {user_id}: {game_info_result['error']}")

                time.sleep(1)
            self.countdown(167)

print_banner()
if __name__ == "__main__":
    client = FreeDogs()
    client.main()
