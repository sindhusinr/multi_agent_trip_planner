from langchain_core.messages import AIMessage


def budget_agent(state: dict) -> dict:
    """
    Calculate trip costs using available structured results.
    """

    print("\n>>> BUDGET AGENT")

    trip_details = state.get("trip_details", {})
    flight_results = state.get("flight_results", {})
    hotel_results = state.get("hotel_results", {})

    budget = trip_details.get("budget", "")

    result = {
        "success": True,
        "user_budget": budget,
        "flight_cost": None,
        "flight_currency": "",
        "hotel_cost_per_night": None,
        "hotel_currency": "",
        "estimated_total": None,
        "total_currency": "",
        "within_budget": None,
        "limitations": []
    }

    # Use the cheapest returned flight option.
    if (
        isinstance(flight_results, dict)
        and flight_results.get("success")
    ):
        flights = flight_results.get("flights", [])

        prices = [
            flight.get("price")
            for flight in flights
            if isinstance(flight.get("price"), (int, float))
        ]

        if prices:
            result["flight_cost"] = min(prices)
            result["flight_currency"] = flight_results.get(
                "currency",
                ""
            )

    # Use the lowest available hotel price.
    if (
        isinstance(hotel_results, dict)
        and hotel_results.get("success")
    ):
        hotels = hotel_results.get("hotels", [])

        hotel_prices = [
            hotel.get("price_min")
            for hotel in hotels
            if isinstance(
                hotel.get("price_min"),
                (int, float)
            )
        ]

        if hotel_prices:
            result["hotel_cost_per_night"] = min(
                hotel_prices
            )

            cheapest_hotel = min(
                hotels,
                key=lambda hotel: (
                    hotel.get("price_min")
                    if isinstance(
                        hotel.get("price_min"),
                        (int, float)
                    )
                    else float("inf")
                )
            )

            result["hotel_currency"] = (
                cheapest_hotel.get("currency", "")
            )

    # Never combine prices with different currencies.
    if (
        result["flight_cost"] is not None
        and result["hotel_cost_per_night"] is not None
    ):
        if (
            result["flight_currency"]
            == result["hotel_currency"]
        ):
            result["limitations"].append(
                "Hotel duration is required before a "
                "complete accommodation cost can be calculated."
            )
        else:
            result["limitations"].append(
                "Flight and hotel prices use different "
                "currencies, so they were not combined."
            )

    if result["flight_cost"] is None:
        result["limitations"].append(
            "Flight cost is unavailable."
        )

    if result["hotel_cost_per_night"] is None:
        result["limitations"].append(
            "Hotel cost is unavailable."
        )

    if not budget:
        result["limitations"].append(
            "No user budget was provided, so affordability "
            "cannot be evaluated."
        )

    return {
        "budget_results": result,
        "messages": [
            AIMessage(
                content="Budget calculation completed."
            )
        ]
    }