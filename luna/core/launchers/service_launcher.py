
WEATHER = "weather"
TEMPERATURE = "temperature"
HUMIDITY = "humidity"
TIMER = "timer"
VOLUME = "volume"
TIME = "time"

def launch_timer(message, cheetah):
    pass

def launch_weather(message, cheetah):
    pass

def launch_clock(message, cheetah):
    pass

def launch_indoor_hum(message, cheetah):
    pass

def launch_volume(message, cheetah):
    pass

services = {
    WEATHER: launch_weather,
    TEMPERATURE: launch_weather,
    HUMIDITY: launch_indoor_hum,
    TIMER: launch_timer,
    VOLUME:launch_volume,
    TIME: launch_clock,
}

def launch_service(service_command, message, cheetah):
    service = services.get(service_command)
    if service:
        service(message, cheetah)
