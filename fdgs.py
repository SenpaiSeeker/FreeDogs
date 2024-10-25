import os
import json
import time
import requests
import hashlib
import logging
from datetime import datetime
from luxon import DateTime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Headers configuration equivalent to the original JavaScript code
DEFAULT_HEADERS = {
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


class FreeDogs:
    def __init__(self):
        self.headers = DEFAULT_HEADERS.copy()

    async def countdown(self, seconds):
        for i in range(seconds, -1, -1):
            print(f"\rWait {i} seconds to continue the loop", end="")
            await time.sleep(1)
        logger.info("")

    async def call_api(self, init_data):
        url = f"https://api.freedogs.bot/miniapps/api/user/telegram_auth?invitationCode=oscKOfyL&initData={init_data}"
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200 and data["code"] == 0:
                return {"success": True, "data": data["data"]}
            else:
                return {"success": False, "error": data["msg"]}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    def is_expired(self, token):
        header, payload, signature = token.split(".")
        decoded_payload = json.loads(base64.urlsafe_b64decode(payload + "==").decode("utf-8"))
        current_timestamp = int(datetime.now().timestamp())

        if "exp" in decoded_payload:
            expiration_date = datetime.fromtimestamp(decoded_payload["exp"])
            logger.info(f"Token expires on: {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}")
            is_expired = current_timestamp > decoded_payload["exp"]
            logger.info("Has the token expired? {}".format(
                "Yes, you need to replace the token" if is_expired else "Not yet, you can continue using the token"
            ))
            return is_expired
        else:
            logger.warning("Perpetual token, expiration time cannot be read")
            return False

    async def get_game_info(self, token):
        url = "https://api.freedogs.bot/miniapps/api/user_game_level/GetGameInfo?"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200 and data["code"] == 0:
                game_info = data["data"]
                logger.info(f"The current balance: {game_info['currentAmount']}")
                logger.info(f"Coin Pool: {game_info['coinPoolLeft']}/{game_info['coinPoolLimit']}")
                logger.info(f"Number of clicks today: {game_info['userToDayNowClick']}/{game_info['userToDayMaxClick']}")
                return {"success": True, "data": game_info}
            else:
                return {"success": False, "error": data["msg"]}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    def md5(self, input_str):
        return hashlib.md5(input_str.encode("utf-8")).hexdigest()

    async def collect_coin(self, token, game_info):
        url = "https://api.freedogs.bot/miniapps/api/user_game/collectCoin"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        collect_amount = min(game_info["coinPoolLeft"], 10000 - game_info["userToDayNowClick"])
        collect_seq_no = int(game_info["collectSeqNo"])
        hash_code = self.md5(f"{collect_amount}{collect_seq_no}7be2a16a82054ee58398c5edb7ac4a5a")

        params = {
            "collectAmount": collect_amount,
            "hashCode": hash_code,
            "collectSeqNo": collect_seq_no
        }
        try:
            response = requests.post(url, data=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200 and data["code"] == 0:
                logger.info(f"Successfully collected {collect_amount} coins")
                return {"success": True, "data": data["data"]}
            else:
                return {"success": False, "error": data["msg"]}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    async def get_task_list(self, token):
        url = "https://api.freedogs.bot/miniapps/api/task/lists?"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200 and data["code"] == 0:
                tasks = [task for task in data["data"]["lists"] if task["isFinish"] == 0]
                return {"success": True, "data": tasks}
            else:
                return {"success": False, "error": data["msg"]}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    async def complete_task(self, token, task_id):
        url = f"https://api.freedogs.bot/miniapps/api/task/finish_task?id={task_id}"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {"success": True} if response.status_code == 200 and data["code"] == 0 else {"success": False, "error": data["msg"]}
        except requests.RequestException as error:
            return {"success": False, "error": str(error)}

    async def process_tasks(self, token, user_id):
        task_list_result = await self.get_task_list(token)
        if task_list_result["success"]:
            for task in task_list_result["data"]:
                logger.info(f"Performing task: {task['name']}")
                complete_result = await self.complete_task(token, task["id"])
                if complete_result["success"]:
                    logger.info(f"Completed task {task['name']} successfully | Reward: {task['rewardParty']}")
                else:
                    logger.error(f"Cannot complete task {task['name']}: {complete_result['error']}")
                time.sleep(1)
        else:
            logger.error(f"Unable to get task list for account {user_id}: {task_list_result['error']}")

    async def main(self):
        token_file = "token.json"
        data_file = "data.txt"

        tokens = json.load(open(token_file)) if os.path.exists(token_file) else {}

        with open(data_file, "r") as file:
            data = [line.strip() for line in file if line.strip()]

        while True:
            for i, raw_init_data in enumerate(data):
                init_data = raw_init_data.replace("&", "%26").replace("=", "%3D")
                user_data_str = json.loads(init_data.split("user%3D")[1].split("%26")[0])
                user_id = user_data_str["id"]
                first_name = user_data_str["first_name"]

                logger.info(f"Account {i + 1} | {first_name}")

                token = tokens.get(user_id)
                if not token or self.is_expired(token):
                    logger.info(f"Need to get new token for account {user_id}...")
                    api_result = await self.call_api(init_data)

                    if api_result["success"]:
                        logger.info(f"Successfully obtained token for account {user_id}")
                        tokens[user_id] = api_result["data"]["token"]
                        token = api_result["data"]["token"]
                        json.dump(tokens, open(token_file, "w"), indent=2)
                        logger.info(f"New token has been saved for account {user_id}")
                    else:
                        logger.error(f"Failed to get token for account {user_id}: {api_result['error']}")
                        continue

                game_info_result = await self.get_game_info(token)
                if game_info_result["success"]:
                    if game_info_result["data"]["coinPoolLeft"] > 0:
                        await self.collect_coin(token, game_info_result["data"])
                    else:
                        logger.warning(f"No coins to collect for account {user_id}")
                    await self.process_tasks(token, user_id)
                else:
                    logger.error(f"Unable to get game information for account {user_id}: {game_info_result['error']}")

                time.sleep(1)

            await self.countdown(167)


if __name__ == "__main__":
    client = FreeDogs()
    asyncio.run(client.main())
