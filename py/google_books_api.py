import os
import json
import requests  
from requests.exceptions import HTTPError


GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
LIST_ISBN = [
    '9780002005883',
    '9780002238304',
    '9780002261982',
    '9780006163831',
    '9780006178736',
    '9780006280897',
    '9780006280934',
    '9780006353287',
    '9780006380832',
    '9780006470229',
]


def extract_fields_from_response(item):
    volume_info = item.get("volumeInfo", {})
    title = volume_info.get("title", None)
    subtitle = volume_info.get("subtitle", None)
    description = volume_info.get("description", None)
    published_date = volume_info.get("publishedDate", None)
    return (
        title,
        subtitle,
        description,
        published_date,
    )


def get_book_details_seq(isbn, session):
    url = GOOGLE_BOOKS_URL + isbn
    response = None
    try:
        response = session.get(url)
        response.raise_for_status()
        print(f"Response status ({url}): {response.status_code}")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")
    response_json = response.json()
    items = response_json.get("items", [{}])[0]
    return items


with requests.Session() as session:
    for isbn in LIST_ISBN:
        try:
            response = get_book_details_seq(isbn, session)
            parsed_response = extract_fields_from_response(response)
            print(f"Response: {json.dumps(parsed_response, indent=2)}")
        except Exception as err:
            print(f"Exception occured: {err}")
            pass