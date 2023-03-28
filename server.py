import asyncio
import os

async def read_file(file_path):
    file_contents = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            file_contents.append(line.strip())
    return file_contents

async def handle_client(reader, writer):
    curr_dir = os.getcwd()
    while True:
        try:
            data = await reader.readline()
            response = ''
            message = data.decode().strip()
            print(f"Received: {message}")

            if message == 'exit':
                writer.write(b'OK - Closing connection\n')
                writer.close()
                break

            if message[:2] == 'cd':
                if os.path.isdir(os.path.join(curr_dir, message[3:])):
                    curr_dir = os.path.join(curr_dir, message[3:])
                    response = f"OK - Current directory: {curr_dir}"
                else:
                    response = f"ERROR - {message[3:]} is not a directory"

            elif message == 'list':
                response = ','.join(os.listdir(curr_dir))

            elif message[:3] == 'get':
                file_path = os.path.join(curr_dir, message[4:])
                if os.path.isfile(file_path):
                    async with asyncio.create_task(read_file(file_path)) as file_contents:
                        response = ','.join(file_contents)
                else:
                    response = f"ERROR - {message[4:]} is not a file"
            else:
                response = f"ERROR - Unknown command: {message}"
            
            writer.write(response.encode() + b'\n')
            await writer.drain()

        except (ConnectionResetError, BrokenPipeError):
            print("Connection closed")
            break

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())