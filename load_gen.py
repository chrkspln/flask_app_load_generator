import os
import asyncio
import aiohttp
import random
import time

# Environment variables
TARGET_URL = os.getenv("TARGET_URL", "http://51.21.255.185:5000")
REQUESTS_PER_SECOND = int(os.getenv("REQUESTS_PER_SECOND", "20"))
DURATION_SEC = int(os.getenv("DURATION_SEC", "60"))

# Available routes (ID range 1–10)
ROUTES = [
    "/delivery",
    "/price",
    "/product_expiration",
    "/store_supply",
    "/supplier",
    "/product",
]

async def hit(session, url):
    try:
        async with session.get(url) as resp:
            await resp.text()  # discard body, we only care about timing
    except Exception as e:
        print(f"Request failed: {e}")

async def worker(session, rate_limit):
    interval = 1.0 / rate_limit
    end_time = time.time() + DURATION_SEC

    while time.time() < end_time:
        route = random.choice(ROUTES)
        # Some routes with ID
        if random.random() < 0.4:
            route += f"/{random.randint(1,10)}"

        url = f"{TARGET_URL.rstrip('/')}{route}"
        asyncio.create_task(hit(session, url))
        await asyncio.sleep(interval)

async def main():
    concurrency = min(REQUESTS_PER_SECOND * 4, 200)
    print(f"Starting load: {REQUESTS_PER_SECOND} req/s for {DURATION_SEC}s to {TARGET_URL}")
    print(f"Using {concurrency} concurrent workers")

    async with aiohttp.ClientSession() as session:
        tasks = [worker(session, REQUESTS_PER_SECOND / concurrency) for _ in range(concurrency)]
        await asyncio.gather(*tasks)

    print("Load test completed.")

if __name__ == "__main__":
    asyncio.run(main())
