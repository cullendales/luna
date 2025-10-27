from core.services.news import get_news
from core.services.time.clock import get_time

WEATHER = "weather"
TEMPERATURE = "temperature"
HUMIDITY = "humidity"
TIMER = "timer"
VOLUME = "volume"
TIME = "time"
NEWS = "news"

def launch_timer(message, cheetah):
    pass

def launch_weather(message, cheetah):
    pass

def launch_clock(message, cheetah):
    get_time()

def launch_indoor_hum(message, cheetah):
    pass

def launch_volume(message, cheetah):
    pass

def launch_news(message, cheetah):
    get_news()

services = {
    WEATHER: launch_weather,
    TEMPERATURE: launch_weather,
    HUMIDITY: launch_indoor_hum,
    TIMER: launch_timer,
    VOLUME:launch_volume,
    TIME: launch_clock,
    NEWS: launch_news,
}

def launch_service(service_command, message, cheetah):
    service = services.get(service_command)
    if service:
        service(message, cheetah)
