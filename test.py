import aiohttp, asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://jsonplaceholder.typicode.com/posts') as resp:
            print(await resp.json())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())