import asyncio
import aioconsole

async def read_response(reader):
    response = await reader.readline()
    return response.decode().strip().split(',')

async def write_message(writer):
    message = await aioconsole.ainput("> ")
    writer.write(message.encode() + b'\n')
    await writer.drain()
    return message

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    while True:
        message = await write_message(writer)

        response_lines = await read_response(reader)
        for line in response_lines:
            print(line)

        if message.strip() == 'exit':
            break
        
    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(asyncio.gather(main()))