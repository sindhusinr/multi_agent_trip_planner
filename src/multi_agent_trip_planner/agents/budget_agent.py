from langchain_core.messages import AIMessage


def budget_agent(state: dict) -> dict:
    """
    Budget analysis specialist.

    Reviews trip affordability using
    available trip details and agent outputs.
    """

    trip_details = state.get(
        "trip_details",
        {}
    )

    destination = trip_details.get(
        "destination",
        ""
    )

    duration = trip_details.get(
        "duration",
        ""
    )

    budget = trip_details.get(
        "budget",
        ""
    )

    travel_style = trip_details.get(
        "travel_style",
        ""
    )

    flight_results = state.get(
        "flight_results",
        ""
    )

    hotel_results = state.get(
        "hotel_results",
        ""
    )

    review = []

    review.append("=== BUDGET REVIEW ===\n")

    review.append(
        f"Destination: {destination or 'Not Provided'}"
    )

    review.append(
        f"Duration: {duration or 'Not Provided'}"
    )

    review.append(
        f"Budget: {budget or 'Not Provided'}"
    )

    review.append(
        f"Travel Style: {travel_style or 'Not Provided'}"
    )

    review.append("\nTrip Assessment")

    # ==========================================================
    # WHY:
    # Budget analysis is useless if budget
    # itself is missing.
    # ==========================================================
    if not budget:

        review.append(
            "- No budget has been provided."
        )

        review.append(
            "- Please specify a budget for meaningful cost analysis."
        )

        budget_results = "\n".join(review)

        return {
            "budget_results": budget_results,
            "messages": [
                AIMessage(
                    content="Budget analysis generated."
                )
            ]
        }

    review.append(
        "- Budget information has been captured."
    )

    # ==========================================================
    # WHY:
    # Longer trips generally increase
    # accommodation, food and transport costs.
    # ==========================================================
    if duration:

        review.append(
            "- Trip duration is available and should be considered when estimating overall trip expenses."
        )

    else:

        review.append(
            "- Trip duration was not provided."
        )

        review.append(
            "- Total trip cost cannot be estimated accurately without a duration."
        )

    # ==========================================================
    # Flight Analysis
    # ==========================================================
    if not flight_results:

        review.append(
            "- Flight information is unavailable."
        )

    elif (
        "No flights found" in flight_results
        or "Unable to find airport code"
        in flight_results
        or "Flight API error"
        in flight_results
    ):

        review.append(
            "- Flight costs cannot currently be estimated because no flight information was found."
        )

    else:

        review.append(
            "- Flight options are available and should be included in final trip budgeting."
        )

    # ==========================================================
    # Hotel Analysis
    # ==========================================================
    if hotel_results:

        review.append(
            "- Hotel recommendations are available."
        )

        review.append(
            "- Accommodation will likely be one of the largest trip expenses."
        )

    else:

        review.append(
            "- Hotel information is unavailable."
        )

    # ==========================================================
    # Travel Style Review
    # ==========================================================
    if travel_style:

        style = travel_style.lower()

        if style == "luxury":

            review.append(
                "- Luxury travel typically increases accommodation and activity expenses."
            )

        elif style == "budget":

            review.append(
                "- Budget travel can significantly reduce overall trip costs."
            )

        elif style == "family":

            review.append(
                "- Family travel may increase accommodation and transportation costs."
            )

    # ==========================================================
    # Budget Recommendations
    # ==========================================================
    review.append("\nRecommendations")

    review.append(
        "- Reserve 10% to 15% of the budget as an emergency fund."
    )

    review.append(
        "- Include accommodation, food, local transport and activity costs."
    )

    review.append(
        "- Keep a contingency amount for unexpected expenses."
    )

    review.append(
        "- Verify foreign exchange requirements before international travel."
    )

    review.append(
        "- Purchase travel insurance when travelling internationally."
    )

    budget_results = "\n".join(review)

    return {
        "budget_results": budget_results,
        "messages": [
            AIMessage(
                content="Budget analysis generated."
            )
        ]
    }