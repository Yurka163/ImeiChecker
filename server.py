import logging
import uvicorn
from imei import get_imei_info, validate_imei
from bot import start_bot
import asyncio
from fastapi import FastAPI, Request, HTTPException

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post('/api/check-imei')
async def check(request: Request):
    try:
        data = await request.json()
        if not data.get("deviceId") or not data.get("token"):
            logging.warning("Не достаточно данных в запросе")
            raise HTTPException(status_code=400, detail="Недостаточно данных в запросе")

        if not validate_imei(data["deviceId"]):
            raise HTTPException(status_code=400, detail="Некорректный IMEI")

        return await get_imei_info(data["deviceId"], data["token"])

    except Exception as e:
        logging.error(f"Ошибка: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


async def run_server():
    config = uvicorn.Config(
        app=app,
        host="localhost",
        port=5000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(
        run_server(),
        start_bot()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Приложение остановлено")
