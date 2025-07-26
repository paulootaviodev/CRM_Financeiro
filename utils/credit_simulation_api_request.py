import requests

def send_data_to_api(data, api_url):
    """
    Sends a dictionary of data to a specified API endpoint via POST request.

    Parameters:
    - data: dictionary containing the payload fields
    - api_url: the endpoint URL of the API

    Returns:
    - response: the response object returned by the API
    """

    # Set headers indicating the request and response content type
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Send POST request with data payload and headers
    response = requests.post(api_url, json=data, headers=headers)
    return response
