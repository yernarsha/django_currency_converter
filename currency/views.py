from django.shortcuts import render

import json
import requests
import os

# Create your views here.

def currency_data():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'currencies.json')

    with open(file_path, "r") as f:
        currency_data = json.loads(f.read())

    return currency_data


def index(request):   
    if request.method == "POST":
        amount = float(request.POST.get('amount'))
        currency_from = request.POST.get("currency_from")
        currency_to = request.POST.get("currency_to")

        url = f"https://v6.exchangerate-api.com/v6/4fe21c60e62b078b34d5dd73/latest/{currency_from}"
        d = requests.get(url).json()

        if d["result"] == "success":        
            ex_target = d["conversion_rates"][currency_to]
            result = ex_target * amount
            result = "{:.2f}".format(result)

            context = {
            "result": result, 
            "currency_to": currency_to, 
            "currency_data": currency_data(),
            "source": str(amount) + " " + currency_from,
            }

            return render(request, "currency/index.html", context)

    return render(request, "currency/index.html", {"currency_data": currency_data()})