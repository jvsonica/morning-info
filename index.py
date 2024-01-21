from weather import fetch_weather

predictions = fetch_weather()

for p in predictions:
    print(f'{p['icon']}   {p['day']} at {p['hour']}:00   {p['description']}   🌡 {p['temperature']}°  💧 {p['precipMM']}mm')
