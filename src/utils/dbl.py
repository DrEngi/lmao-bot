import aiohttp
import asyncio
import socket
import io

with io.open("tokens/lmao-dbl.txt", "r") as token:
    dbl_token = (token.read()).strip()
dbl_headers = {"Authorization" : dbl_token}

async def has_voted(user_id):
    dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True,use_dns_cache=False)
    vote_url = f"https://discordbots.org/api/bots/459432854821142529/check?userId={user_id}"
    async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
        async with aioclient.get(vote_url, headers=dbl_headers) as r:
            vote_data = await r.json()
            if vote_data["voted"] == 0:
                return False
            return True
