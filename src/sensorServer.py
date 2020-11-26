import asyncio
import sensorIO
import pickle

sensors = sensorIO.Sensors()
sensorLock = asyncio.Lock()

async def handle_echo(reader, writer):
    while not reader.at_eof():
        data = await reader.read(1)
        sensor_type = data.decode()

        addr = writer.get_extra_info('peername')
        print(f"Received {sensor_type!r} from {addr!r}")

        if sensor_type == "I":
            imuData = None
            async with sensorLock:
                imuData = sensors.getImuData()
            imuPickle = pickle.dumps(imuData)
            print(f"Sending imu data length.")
            # Send length of data
            writer.write(len(imuPickle).to_bytes(2, byteorder='big'))
            print(f"Sending imu data.")
            # Send the data
            writer.write(imuPickle)
            await writer.drain()
        elif sensor_type == "A":
            altData = None
            async with sensorLock:
                altData = sensors.getAltData()
            print(f"Sending alt data length.")
            altPickle = pickle.dumps(altData)
            # Send length of data
            writer.write(len(altPickle).to_bytes(2, byteorder='big'))
            print(f"Sending alt data.")
            # Send the data
            writer.write(altPickle)
            await writer.drain()
        else:
            print("Close the connection")
            writer.close()


async def main():
    server = await asyncio.start_unix_server(
        handle_echo, './mysocket')

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
