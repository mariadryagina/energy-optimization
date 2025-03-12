import pandas as pd
from entsoe import EntsoePandasClient
from datetime import datetime, timedelta
import pytz

API_token='c2eaefad-f105-486d-9ba1-1472bc376302'

def read_spot_price(dt_start, dt_end):
    client = EntsoePandasClient(api_key=API_token)
    start_datetime = pd.Timestamp(dt_start)
    end_datetime = pd.Timestamp(dt_end)
    country_code = 'SE_3'
    DA_prices = client.query_day_ahead_prices(country_code, start=start_datetime, end=end_datetime)
    eur_to_sek = 11.07  # on 2022-09-19
    mwh_to_kwh = 1000
    DA_prices = DA_prices * eur_to_sek / mwh_to_kwh
    return DA_prices

def read_generation(dt_start, dt_end,country):
    client = EntsoePandasClient(api_key=API_token)
    start_datetime = pd.Timestamp(dt_start)
    end_datetime = pd.Timestamp(dt_end)
    country_code = 'SE_3'
    country_code = country
    Production = client.query_generation(country_code, start=start_datetime, end=end_datetime)
    return Production

def read_load(dt_start, dt_end,country):
    client = EntsoePandasClient(api_key=API_token)
    start_datetime = pd.Timestamp(dt_start)
    end_datetime = pd.Timestamp(dt_end)
    country_code = 'SE_3'
    country_code = country
    Load = client.query_load(country_code, start=start_datetime, end=end_datetime)
    return Load

start = datetime.strptime("2024-01-01 00:00", "%Y-%m-%d %H:%M")
end = datetime.strptime("2024-12-31 23:59", "%Y-%m-%d %H:%M")
timezone = pytz.timezone("UTC")
start = timezone.localize(start)
end = timezone.localize(end)
DA_pricesdata = read_spot_price(start, end)  # SEK/kWh
DA_pricesdata.to_csv('price_2024.csv')
