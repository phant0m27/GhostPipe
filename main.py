import asyncio
from scrapers import FreeProxyListParser
from checker import ProxyChecker

async def main():
    print("=== PhantomProxy Start ===")
    parser = FreeProxyListParser()
    raw_list = await parser.fetch()

    if not raw_list:
        print("Не удалось получить прокси.")
        return
    checker = ProxyChecker(raw_list)
    valid_list = await checker.run_checker()



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Проверка прервана пользователем. Все найденные прокси сохранены в proxy.txt")