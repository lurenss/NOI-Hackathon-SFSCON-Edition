import asyncio
from main import query_fluxdb  # Import the function from the first file

async def main():
    while True:
        print("Calling query_fluxdb()...")
        await query_fluxdb()
        await asyncio.sleep(5)  # Wait for 5 seconds before the next call

if __name__ == "__main__":
        asyncio.run(main())
