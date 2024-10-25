import os
import json
import time
import hashlib
import requests
from datetime import datetime
from dateutil import parser as date_parser
import logging
import urllib.parse


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


# Configure logger with detailed format similar to Winston
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger()

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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

    def countdown(self, seconds):
        """Countdown function to wait before the next loop iteration."""
        for i in range(seconds, -1, -1):
            print(f"\rWait {i} seconds to continue the loop", end="")
            time.sleep(1)
        logger.info("")

    def call_api(self, init_data):
        """Call API with the invitation code and init data."""
        url = f"https://api.freedogs.bot/miniapps/api/user/telegram_auth?invitationCode=oscKOfyL&initData={init_data}"
        try:
            response = requests.post(url, headers=self.headers)
            if response.status_code == 200 and response.json().get("code") == 0:
                return {"success": True, "data": response.json().get("data")}
            else:
                return {"success": False, "error": response.json().get("msg")}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    def is_expired(self, token):
        """Check if a given JWT token is expired."""
        try:
            payload = token.split(".")[1]
            decoded_payload = json.loads(
                base64.urlsafe_b64decode(payload + "==").decode("utf-8")
            )
            now = int(datetime.now().timestamp())

            if "exp" in decoded_payload:
                expiration_date = datetime.fromtimestamp(decoded_payload["exp"])
                logger.info(f"Token expires on: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}")

                is_expired = now > decoded_payload["exp"]
                logger.info(f"Has the token expired? {'Yes' if is_expired else 'No'}")
                return is_expired
            else:
                logger.warning("Perpetual token, expiration time cannot be read")
                return False
        except Exception as error:
            logger.error(f"Error: {str(error)}")
            return True

    def get_game_info(self, token):
        """Retrieve game information from the API."""
        url = "https://api.freedogs.bot/miniapps/api/user_game_level/GetGameInfo?"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200 and response.json().get("code") == 0:
                data = response.json().get("data")
                logger.info(f"The current balance: {data['currentAmount']}")
                logger.info(f"Coin Pool: {data['coinPoolLeft']}/{data['coinPoolLimit']}")
                logger.info(f"Number of clicks today: {data['userToDayNowClick']}/{data['userToDayMaxClick']}")
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": response.json().get("msg")}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    def md5(self, input_str):
        """Generate MD5 hash of input string."""
        return hashlib.md5(input_str.encode()).hexdigest()

    def collect_coin(self, token, game_info):
        """Collect coins using the game information."""
        url = "https://api.freedogs.bot/miniapps/api/user_game/collectCoin"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}

        collect_amount = min(game_info["coinPoolLeft"], 10000 - game_info["userToDayNowClick"])
        collect_seq_no = int(game_info["collectSeqNo"])
        hash_code = self.md5(f"{collect_amount}{collect_seq_no}7be2a16a82054ee58398c5edb7ac4a5a")

        data = {
            "collectAmount": collect_amount,
            "hashCode": hash_code,
            "collectSeqNo": collect_seq_no,
        }

        try:
            response = requests.post(url, data=data, headers=headers)
            if response.status_code == 200 and response.json().get("code") == 0:
                logger.info(f"Successfully collected {collect_amount} coins")
                return {"success": True, "data": response.json().get("data")}
            else:
                return {"success": False, "error": response.json().get("msg")}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    def get_task_list(self, token):
        """Retrieve the list of tasks from the API."""
        url = "https://api.freedogs.bot/miniapps/api/task/lists?"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200 and response.json().get("code") == 0:
                tasks = [task for task in response.json()["data"]["lists"] if task["isFinish"] == 0]
                return {"success": True, "data": tasks}
            else:
                return {"success": False, "error": response.json().get("msg")}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    def complete_task(self, token, task_id):
        """Complete a specific task by ID."""
        url = f"https://api.freedogs.bot/miniapps/api/task/finish_task?id={task_id}"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}

        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200 and response.json().get("code") == 0:
                return {"success": True}
            else:
                return {"success": False, "error": response.json().get("msg")}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    def process_tasks(self, token, user_id):
        """Process the tasks for a specific user."""
        task_list_result = self.get_task_list(token)
        if task_list_result["success"]:
            for task in task_list_result["data"]:
                logger.info(f"Performing task: {task['name']}")
                complete_result = self.complete_task(token, task["id"])
                if complete_result["success"]:
                    logger.info(f"Completed task {task['name']} successfully")
                else:
                    logger.error(f"Cannot complete task {task['name']}: {complete_result['error']}")
                time.sleep(1)
        else:
            logger.error(f"Unable to get task list for account {user_id}: {task_list_result['error']}")

    def main(self):
        """Main loop for processing users and tokens."""
        data_file = os.path.join(os.getcwd(), "data.txt")
        token_file = os.path.join(os.getcwd(), "token.json")
        
        # Load tokens from file
        tokens = {}
        if os.path.exists(token_file):
            with open(token_file, "r") as f:
                tokens = json.load(f)
        
        with open(data_file, "r") as f:
            data = [line.strip() for line in f if line.strip()]
        
        while True:
            for i, raw_init_data in enumerate(data):
                init_data = urllib.parse.quote(raw_init_data)
                user_data_str = urllib.parse.unquote(init_data.split("user%3D")[1].split("%26")[0])
                user_data = json.loads(urllib.parse.unquote(user_data_str))
                user_id = user_data["id"]
                first_name = user_data["first_name"]

                logger.info(f"Account {i + 1} | {first_name}")

                token = tokens.get(user_id)
                need_new_token = not token or self.is_expired(token)

                if need_new_token:
                    logger.info(f"Need to get new token for account {user_id}...")
                    api_result = self.call_api(init_data)

                    if api_result["success"]:
                        logger.info(f"Successfully obtained token for account {user_id}")
                        tokens[user_id] = api_result["data"]["token"]
                        token = api_result["data"]["token"]
                        with open(token_file, "w") as f:
                            json.dump(tokens, f, indent=2)
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

if __name__ == "__main__":
    print_banner()
    client = FreeDogs()
    try:
        client.main()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        exit(1)
