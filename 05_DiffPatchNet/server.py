import asyncio
from cowsay import cowsay, list_cows

cows_names = list_cows()
clients = {}

async def chat(reader, writer):
    me = writer.get_extra_info('peername')
    cow_name = None

    async def handle_message(sender, receiver, message):
        '''
        Prints user's message
        '''
        if receiver in clients:
            clients[receiver].write(
                    f"{sender} says: {message}\n".encode()
                )
            await clients[receiver].drain()

    async def list_users():
        '''
        List\'s all users, that are online
        '''
        writer.write(
                ("Users online:\n" + "\n".join([f"- {name}" 
                    for name in clients.keys()]) + "\n"
                ).encode()
            )
        await writer.drain()

    # MAIN LOOP
    while not reader.at_eof():
        command = (await reader.readline()).decode().strip().split()

        # List valid usernames
        if command[0] == "cows":
            output = "Available cow names:\n" + "\n".join(cows_names) + "\n"
            writer.write(
                (output).encode()
            )
            await writer.drain()

        # List online users
        elif command[0] == "who":
            await list_users()
   
        # Registration to the chat
        elif command[0] == "login":
            if len(command) > 1 and command[1] not in clients.values():
                cow_name = command[1]
                clients[cow_name] = writer
                writer.write(
                    f"You are now logged in as {cow_name}\n".encode()
                )
                await writer.drain()
            else:
                writer.write(
                    "Cow name already taken or not provided\n".encode()
                )
                await writer.drain()

        # Send a message to a user
        elif command[0] == "say":
            if cow_name:
                await handle_message(
                        sender=cow_name, 
                        receiver=command[1], 
                        message=" ".join(command[2:])
                    )
            else:
                writer.write(
                    "You need to log in before sending messages\n".encode()
                )
                await writer.drain()

        # Send a message to all users 
        elif command[0] == "yield":
            if cow_name:
                for name in clients.keys():
                    if name != cow_name:
                        await handle_message(
                                sender=cow_name, 
                                receiver=name, 
                                message=" ".join(command[1:])
                            )

        # Log out from the chat
        elif command[0] == "quit":
            if cow_name:
                del clients[cow_name]
                writer.write(
                    "You have been disconnected\n".encode()
                )
                await writer.drain()
                break

        # All other cases for commands
        else:
            writer.write("Unknown command\n".encode())
            await writer.drain()

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
