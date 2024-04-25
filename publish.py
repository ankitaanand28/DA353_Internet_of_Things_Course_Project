import network
import time
import utime
import urandom
from umqtt.simple import MQTTClient
import ubinascii
import machine

# MQTT broker configuration
SERVER = b"f2a2c50d3bf143cb86d175f6306f9781.s1.eu.hivemq.cloud"
PORT = 0
USERNAME = b"Nodes"
PASSWORD = b"Nodes@123"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
PUBLISH_TOPIC = b"SensorData"  # Changed the topic to generalize it for all sensor data

# WiFi configuration
WIFI_SSID = "Professor"
WIFI_PASSWORD = "123456789"

def connect_to_wifi(ssid, password):
    # Configure WiFi using Station Interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('WiFi connected:', wlan.ifconfig())
    return wlan

def generate_random_within_range(min_value, max_value):
    return urandom.randint(min_value, max_value + 1)  # Adjusted to include the upper bound

def generate_ph_value():
    # Generate random pH value within the specified range
    ph_mean = 6.5
    ph_range = 3.4  # Half of the range around the mean
    ph_value = min(max(3.3, ph_mean + urandom.getrandbits(5) * ph_range / 512), 9.9)
    # Round the pH value to two decimal places
    return round(ph_value, 2)

def publish_sensor_data(client):
    # Get current time
    current_time = utime.time()
    
    # Statistical details for each parameter
    parameter_ranges = {
        "Temperature": {"mean": 30, "std": 4, "min": 25, "max": 38},
        "Humidity": {"mean": 59, "std": 6, "min": 50, "max": 72},
        "Moisture": {"mean": 43, "std": 12, "min": 25, "max": 65},
        "Nitrogen": {"mean": 19, "std": 12, "min": 4, "max": 42},
        "Potassium": {"mean": 3, "std": 6, "min": 0, "max": 19},
        "Phosphorous": {"mean": 19, "std": 14, "min": 0, "max": 42}
    }
    
    # Generate random values for each parameter within the specified range
    parameter_values = {}
    for parameter, details in parameter_ranges.items():
        # Calculate the range based on mean, std, min, and max
        min_val = details["min"]
        max_val = details["max"]
        mean = details["mean"]
        std = details["std"]
        
        # Generate random value within the range
        value = min(max(min_val, generate_random_within_range(mean - std, mean + std)), max_val)
        parameter_values[parameter] = value
    
    # pH value
    ph = generate_ph_value()
    
    # Publish sensor data values along with current time
    data = {
        "Time": current_time,
        "Temperature": parameter_values["Temperature"],
        "Humidity": parameter_values["Humidity"],
        "Moisture": parameter_values["Moisture"],
        "Nitrogen": parameter_values["Nitrogen"],
        "Potassium": parameter_values["Potassium"],
        "Phosphorous": parameter_values["Phosphorous"],
        "pH": ph
    }
    client.publish(PUBLISH_TOPIC, str(data))
    print("Published sensor data:", data)


if __name__ == '__main__':
    # Connect to WiFi
    wlan = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)

    # Initialize MQTT client with TLS
    c = MQTTClient(CLIENT_ID, SERVER, port=PORT, user=USERNAME, password=PASSWORD, ssl=True, ssl_params={'server_hostname': SERVER})

    try:
        # Connect to MQTT broker
        c.connect()
        print("Connected to MQTT broker:", SERVER)

        while True:
            # Publish sensor data values
            publish_sensor_data(c)
            
            # Delay for 10 seconds
            time.sleep(10)

    except Exception as e:
        print("Error:", e)

    finally:
        # Disconnect MQTT client
        try:
            c.disconnect()
        except:
            pass