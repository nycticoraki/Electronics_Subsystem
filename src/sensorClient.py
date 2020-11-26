import asyncio
import pickle
import sensorData as sd

IMU_DATA = 'I'
ALT_DATA = 'A'

class SensorClient(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.reader, self.writer = self.loop.run_until_complete(asyncio.open_unix_connection('./mysocket'))

    async def _getSensorData(self, message):

        print(f'Send: {message!r}')
        self.writer.write(message.encode())

        data_len_bytes = await self.reader.read(2)
        data_len = int.from_bytes(data_len_bytes,'big')

        data = await self.reader.read(data_len)
        sensor_data = pickle.loads(data)
        return sensor_data

    def getSensorData(self, data_type=IMU_DATA):
        sensor_data = self.loop.run_until_complete(self._getSensorData(data_type))
        return sensor_data

    def close(self):
        print('Close the connection')
        self.writer.close()

if __name__ == '__main__':
    sensorClient = SensorClient()
    imuData = sensorClient.getSensorData(IMU_DATA)
    print('Received: ' + str(imuData))
    altData = sensorClient.getSensorData(ALT_DATA)
    print('Received: ' + str(altData))
    sensorClient.close()
