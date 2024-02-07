import requests
from datetime import datetime
import smtplib
import time

#Fill those with your own data
MY_EMAIL = ""
MY_PASSWORD = ""
SEND_TO_EMAIL = ""

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

def is_ISS_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if 46 <= iss_latitude <= 56 and -5 <= iss_longitude <= 5:
            return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_ISS_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=SEND_TO_EMAIL,
            msg="Subject:Look Up\n\nThe ISS is above you in the sky."
        )
        connection.close()

