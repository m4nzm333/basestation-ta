from gps3 import agps3
import time
from datetime import datetime
gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        lon = None
        lat = None
        if data_stream.lon != "n/a":
            lon = round(float(data_stream.lon), 6)
            lat = round(float(data_stream.lat), 6)
        print('Longitude = ', str(lon))
        print('Latitude = ', str(lat))
        print(str(datetime.now()))
    time.sleep(0.5)