from flask import Flask, request
import weather
import bus

app = Flask(__name__)

@app.route("/")
@app.route("/info")
def api():
    w = weather.fetch_weather()
    b = bus.fetch_next_buses()
    format = request.args.get('format') or request.args.get('as')

    if format == 'json':
        return { 'weather': w, 'bus': b }
   
    bus_info = "".join([
        f"<p>{bus.format(p)}</p>"
        for p in b   
    ])
    weather_info = "".join([
        f"<p>{weather.format(p)}</p>"
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
                display: grid;
                grid-template-columns: 40% 60%;
                grid-column-gap: 5px;
            }}
            h1 {{
                font-size: 0.9em;
                text-align: center;
                color: #333;
                margin: 5px 0;
            }}
            .info-section {{
                background-color: #fff;
                padding: 5px 10px;
                border-radius: 4px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 10px;
            }}
            .bus-info {{
                grid-column: 2;
            }}
            .weather-info {{
                grid-column: 1;
            }}
            p {{
                font-size: 0.9em;
                color: #666;
                margin: 5px 0;
                line-height: 1.4;
            }}
        </style>
    </head>
    <body>
        <div class="info-section weather-info">
            <h1>Weather Information</h1>
            {weather_info}
        </div>
        <div class="info-section bus-info">
            <h1>Bus Information</h1>
            {bus_info}
        </div>
    </body>
    </html>
    """
    return html_response


@app.route("/alive")
def alive():
    return 'Safe and sound!'


if __name__ == "__main__":
    app.run(debug=True)

