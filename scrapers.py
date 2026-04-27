import httpx
import asyncio
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import lxml

class BaseScraper(ABC):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    @abstractmethod
    async def fetch(self) -> list:
        """
        Метод-пустышка. Дочерние классы (парсеры) будут
        реализовывать здесь свою логику.
        """
        pass

    def validate_format(self, proxy: str) -> bool:
        if len(proxy) > 7 and ":" in proxy:
            return True
        else:
            return False

    def clean_proxies(self, raw_list: list) -> list:
        valid_list = [p.strip() for p in raw_list if self.validate_format(p.strip())]
        final_list = list(set(valid_list))
        print(f"[Base] Очищено: {len(final_list)} уникальных прокси")
        return final_list

class FreeProxyListParser(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url = "https://free-proxy-list.net/"

    async def fetch(self) -> list:
        async with httpx.AsyncClient(headers=self.headers) as client:
            try:
                response = await client.get(self.url)
                soup = BeautifulSoup(response.text, 'lxml')
                raw_proxies = []

                table = soup.find('table', class_='table table-striped table-bordered')

                if table:
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        cols = row.find_all("td")
                        if len(cols) >= 2:
                            raw_proxies.append(f"{cols[0].text}:{cols[1].text}")
                return self.clean_proxies(raw_proxies)

            except Exception as e:
                print(f"Ошибка при парсинге {self.url}: {e}")
                return []


