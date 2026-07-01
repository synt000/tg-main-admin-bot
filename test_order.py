import requests

# ပိုမိုသေချာစေရန် localhost ဖြင့် အစားထိုးထားပါသည်
url = "http://localhost:5000/api/submit_order"

payload = {
    "shop_code": "onlineshop_001",
    "customer_info": "Saw Yan Naing (Ph - 0979xxxxxxx)",
    "order_details": "👕 T-Shirt (Size L) - 1 ထည်, 👖 Jeans Pants - 1 ထည်",
    "total_price": "35,000"
}

headers = {
    "Content-Type": "application/json"
}

try:
    print("📡 Sending Test Order Data to API...")
    response = requests.post(url, json=payload, headers=headers)
    print("📊 API Response:", response.json())
except Exception as e:
    print("❌ Error:", e)
