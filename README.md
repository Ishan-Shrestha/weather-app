# weather-app

A small python web app for weather using FLASK:

contains following routes:
- `/` : for lookup and presentation

Themed by using bootstrap

### Features:
- logging
- API lookup

### libararies used:
- flask
- logging
- os
- dotenv
- requests

### To use:
- Install dependencies:

```cli
    pip install -r requirements.txt
```

### API used:
using OpenWeatherMap's API
url: https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

### .env file
OPENWEATHER_API_KEY=your_key_here