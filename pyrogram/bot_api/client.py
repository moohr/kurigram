import httpx


class BotApiClient:
    def __init__(self, bot_token: str, base_url: str = "https://api.telegram.org"):
        self.bot_token = bot_token
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/bot{bot_token}"
        self._client = httpx.AsyncClient(timeout=60)

    async def request(self, method: str, payload: dict | None = None):
        r = await self._client.post(f"{self.api_url}/{method}", json=payload or {})
        r.raise_for_status()
        data = r.json()

        if not data.get("ok"):
            raise RuntimeError(f"Bot API {method} failed: {data}")

        return data.get("result")

    async def close(self):
        await self._client.aclose()
