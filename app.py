from dotenv import load_dotenv
from flask import render_template, Flask, redirect, request
import logging
import os
import requests

# LOGGER SET-UP CONFIGURATIONS

logging.basicConfig(
    filename="info.log",
    format='%(asctime)s %(levelname)s: %(message)s'
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# VARIABLES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_DIR = os.path.join(BASE_DIR, "tasks.json")


# FLASK APP SET-UP
app = Flask(__name__)

load_dotenv()
api_key = os.getenv('OPENWEATHER_API_KEY')


def get_data(city_name):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        try:
            # timeout=5 prevents the code from hanging indefinitely if the API is down
            response = requests.get(url, timeout=5)
            
            # This raises an HTTPError if the status code is 4xx or 5xx (e.g., 404 City Not Found, 401 Unauthorized)
            response.raise_for_status()

            logger.info(f"Successfully retrieved data of {city_name}")
            
            return response.json()

        except requests.exceptions.ConnectionError:
            logger.error('"error": "Network Error", "message": "Could not connect to the server. Check your internet."')
            return {"error": "Network Error", "message": "Could not connect to the server. Check your internet."}
            
        except requests.exceptions.Timeout:
            logger.error('"error": "Timeout Error", "message": "The server took too long to respond."')
            return {"error": "Timeout Error", "message": "The server took too long to respond."}
            
        except requests.exceptions.HTTPError as http_err:
            # Handles 401 (bad key), 404 (bad city), etc.
            logger.error(f'"error": "HTTP Error ({response.status_code})", "message": str(http_err)')
            return {"error": f"HTTP Error ({response.status_code})", "message": str(http_err)}
            
        except requests.exceptions.RequestException as err:
            # Catches any other requests-related error
            logger.error(f'"error": "Request Error", "message": str(err)')
            return {"error": "Request Error", "message": str(err)}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city_name = request.form.get('city','').strip()
        data = get_data(city_name)
        return render_template('index.html', data=data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)