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

def query_date_and_send_emails(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        # if reminder date is today or already passed AND customer did not pay yet then, send reminder.
        if (present >= row["reminder_date"].date() and row["has_paid"] == "no"):
            send_email(
                subject=f'[Swarup Codes Pvt Ltd.] Invoice: {row["invoice_no"]}',
                name=row["name"],
                receiver_email=row["email"],
                due_date=row["due_date"].strftime("%d, %b %Y"), # example: 11, Aug 2024
                invoice_no=row["invoice_no"],
                amount=row["amount"]
            )
            email_counter += 1
    return f"Total email sent: {email_counter}"

df = load_df(URL)
result = query_date_and_send_emails(df)
print(result)

