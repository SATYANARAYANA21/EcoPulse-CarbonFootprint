from backend.app.carbon.calculator import calculate_footprint

inputs = {
    "transport_km_car_petrol": 1000,
    "diet_type": "vegan",
    "consumption_level": "medium",
    "household_size": 2,
    "home_electricity_kwh": 3000
}

res = calculate_footprint(inputs)
print(res)
