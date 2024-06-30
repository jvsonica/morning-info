from flask import Flask, request
import weather
import bus

app = Flask(__name__)

@app.route("/info")
def api():
    w = weather.fetch_weather()
    b = bus.fetch_next_buses()
    format = request.args.get('format') or request.args.get('as')

    if format == 'json':
        return { 'weather': w, 'bus': b }
   
    bus_info = "".join([
        f'<p>🚌 Line {p["line"]}  ⏳ {p["wait_time"]}  ({p["predicted"]})</p>'
        for p in b   
    ])
    weather_info = "".join([
        f"<p>{p['day']} at {p['hour']}:00   🌡 {p['temperature']}°  💧 {p['precipMM']}mm  {p['icon']}  {p['description']}</p>"
        for p in w
    ])

    html_response = f"""
    <html>
    <head>
        <title>Info</title>
         <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            h1 {{
                font-size: 1.2em;
                text-align: center;
                color: #333;
            }}
            p {{
                font-size: 1em;
                color: #666;
                margin: 5px 0;
            }}
            .info-section {{
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Weather</h1>
        {weather_info}
        <h1>Next Bus</h1>
        {bus_info}
    </body>
    </html>
    """
    return html_response


@app.route("/alive")
def alive():
    return 'Safe and sound!'


if __name__ == "__main__":
    app.run(debug=True)

