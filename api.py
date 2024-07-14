import requests

# Replace with your actual API keys and client credentials
amadeus_client_id = 'YOUR_AMADEUS_CLIENT_ID'
amadeus_client_secret = 'YOUR_AMADEUS_CLIENT_SECRET'
booking_api_key = 'YOUR_BOOKING_API_KEY'


def get_amadeus_bearer_token(client_id, client_secret):
    url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')


amadeus_api_key = get_amadeus_bearer_token(amadeus_client_id, amadeus_client_secret)


def search_flights(origin, destination, departure_date):
    url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
    headers = {
        'Authorization': f'Bearer {amadeus_api_key}'
    }
    params = {
        'originLocationCode': origin,
        'destinationLocationCode': destination,
        'departureDate': departure_date,
        'adults': 1
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def search_hotels(location, check_in_date, check_out_date):
    url = f'https://distribution-xml.booking.com/2.1/json/hotels'
    params = {
        'city_ids': location,
        'checkin_date': check_in_date,
        'checkout_date': check_out_date,
        'room_number': 1
    }
    headers = {
        'Authorization': f'Basic {booking_api_key}'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()
