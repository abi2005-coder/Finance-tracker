def simple_insights(transactions):
    category_totals = {}
    monthly_totals = {}

    for t in transactions:
        cat = t.get("category", "Others")
        amt = float(t.get("amount", 0))

        # Sum category totals
        category_totals[cat] = category_totals.get(cat, 0) + amt

        # Extract month name from date (YYYY-MM-DD)
        date = t.get("date", "")
        if len(date) >= 7:
            year, month, _ = date.split("-")
            month_name = {
                "01": "January", "02": "February", "03": "March",
                "04": "April", "05": "May", "06": "June",
                "07": "July", "08": "August", "09": "September",
                "10": "October", "11": "November", "12": "December"
            }.get(month, "Unknown")

            monthly_totals[month_name] = monthly_totals.get(month_name, 0) + amt

    return {
        "monthly": monthly_totals,
        "category_totals": category_totals
    }
