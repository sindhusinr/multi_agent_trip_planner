AIRPORT_MAPPING = {
    "chennai": "MAA",
    "tokyo": "NRT",
    "japan": "NRT",
    "bangkok": "BKK",
    "singapore": "SIN",
    "dubai": "DXB",
    "paris": "CDG",
    "london": "LHR",
    "new york": "JFK",
}


def get_iata(location: str) -> str:
    return AIRPORT_MAPPING.get(location.lower(), "")