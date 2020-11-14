from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

notification_manager = NotificationManager()
data_manager = DataManager()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "LON"

sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today,
    )

    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! "
                    f"Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} "
                    f"to {flight.destination_city}-{flight.destination_airport}, "
                    f"from {flight.out_date} to {flight.return_date}."
        )