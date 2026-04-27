import httpx
import asyncio
import time

class ProxyChecker:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.test_url = "http://httpbin.org/ip"
        self.valid_proxies = []

    async def check_single_proxy(self, proxy: str):
        proxy_url = f"http://{proxy}"

        start = time.perf_counter()

        try:
            async with httpx.AsyncClient(proxy=proxy_url, timeout=5.0) as client:
                response = await client.get(self.test_url)

                if response.status_code == 200:
                    latency = time.perf_counter() - start
                    with open('proxy.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{proxy}\n")
                    print(f"✅ {proxy} | {latency:.2f}s")
                    return {"proxy": proxy, "latency": latency}

        except Exception as e:
            print(f"❌ {proxy} | Failed")
            return None
    async def run_checker(self) -> list:
        semaphore = asyncio.Semaphore(10)
        async def sem_task(p):
            async with semaphore:
                return await self.check_single_proxy(p)

        print(f"Начинаю проверку {len(self.proxy_list)} прокси...")
        tasks = [sem_task(p) for p in self.proxy_list]

        results = await asyncio.gather(*tasks)
        tasks = [self.check_single_proxy(p) for p in self.proxy_list]
        results = await asyncio.gather(*tasks)
        self.valid_proxies = [r for r in results if r is not None]
        self.valid_proxies.sort(key=lambda x: x['latency'])
        print(f"Проверка завершена. Найдено живых: {len(self.valid_proxies)}")
        return self.valid_proxies