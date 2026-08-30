AIRPORT_MAPPING = {

    # India
    "chennai": "MAA",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "mumbai": "BOM",
    "delhi": "DEL",
    "hyderabad": "HYD",
    "kolkata": "CCU",
    "pune": "PNQ",
    "ahmedabad": "AMD",
    "kochi": "COK",

    # Asia
    "tokyo": "NRT",
    "osaka": "KIX",
    "seoul": "ICN",
    "bangkok": "BKK",
    "singapore": "SIN",
    "kuala lumpur": "KUL",
    "hong kong": "HKG",
    "dubai": "DXB",

    # Europe
    "paris": "CDG",
    "london": "LHR",
    "rome": "FCO",
    "berlin": "BER",
    "amsterdam": "AMS",
    "zurich": "ZRH",

    # North America
    "new york": "JFK",
    "los angeles": "LAX",
    "toronto": "YYZ",

    # Oceania
    "sydney": "SYD",
    "melbourne": "MEL",
}


def get_iata(location: str) -> str:
    return AIRPORT_MAPPING.get(location.lower(), "")