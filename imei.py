import aiohttp
from config_reader import config
import random

API_KEY = config.api_key.get_secret_value()


def validate_imei(imei: str) -> bool:
    if len(imei) != 15 or not imei.isdigit():
        return False
    else:
        return True


async def get_service(token: str):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {token}"}
            async with session.get("https://api.imeicheck.net/v1/services", headers=headers) as response:
                data = await response.json()
                ids = [item["id"] for item in data if "id" in item]
                return random.choice(ids)
    except aiohttp.ClientError as e:
        return {"error": f"Ошибка запроса: {str(e)}"}


async def get_imei_info(imei: str, token: str):
    service_id = await get_service(token)
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {token}"}
            payload = {"deviceId": imei, "serviceId": service_id}

            async with session.post("https://api.imeicheck.net/v1/checks/",
                                    headers=headers, json=payload) as response:
                return await response.json()
    except aiohttp.ClientError as e:
        return {"error": f"Ошибка запроса: {str(e)}"}
