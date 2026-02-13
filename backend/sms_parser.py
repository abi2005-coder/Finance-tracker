import re

def parse_sms(sms_text: str):
    sms = sms_text.lower()

    # Extract amount
    amt_pattern = r"(?:rs\.?|inr|rupees)\s?(\d+[\.,]?\d*)"
    match = re.search(amt_pattern, sms)
    amount = None
    if match:
        amount = float(match.group(1).replace(',', '.'))

    keywords = {
        "swiggy": "food",
        "zomato": "food",
        "uber": "travel",
        "ola": "travel",
        "rapido": "travel",
        "amazon": "shopping",
        "myntra": "shopping",
        "flipkart": "shopping",
        "fuel": "transport",
        "petrol": "transport",
        "rent": "rent",
        "fee": "education"
    }

    category = "others"
    for key, cat in keywords.items():
        if key in sms:
            category = cat
            break

    return {
        "amount": amount,
        "category": category,
        "message": sms_text,
        "date": ""
    }
