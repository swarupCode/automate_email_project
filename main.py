from datetime import date
import pandas as pd #pip3 install pandas
from send_email import send_email


# Public GoogleSheets url - not secure!
SHEET_ID = "1Rf4plC0h0yDw6xGvIFcTSD_5ks-hMGH1M_mjz67Kw40"
SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    parse_dates = ["due_date", "reminder_date"]
    df = pd.read_csv(url, parse_dates=parse_dates)
    return df

print(load_df(URL))