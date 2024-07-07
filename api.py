import requests


def search_flights(origin, destination, departure_date):
    api_key = 'YOUR_API_KEY'
    url = f'https://api.skyscanner.net/apiservices/browseroutes/v1.0/US/USD/en-US/{origin}/{destination}/{departure_date}'
    response = requests.get(url, headers={'api-key': api_key})
    return response.json()


def search_hotels(location, check_in_date, check_out_date):
    api_key = 'YOUR_API_KEY'
    url = f'https://api.hotels.com/v1/search?location={location}&check_in={check_in_date}&check_out={check_out_date}'
    response = requests.get(url, headers={'api-key': api_key})
    return response.json()
