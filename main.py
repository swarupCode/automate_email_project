from datetime import date, timedelta
import datetime
import pandas as pd #pip3 install pandas
from send_email import send_email_for_pm
from send_email import send_email_for_amc
from enum import Enum

# Query 1: If the code fails on the day of sending message - keep a DB

# Public GoogleSheets url - not secure!
SHEET_ID = "1Rf4plC0h0yDw6xGvIFcTSD_5ks-hMGH1M_mjz67Kw40"
SHEET_NAME = "Sheet2"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

class Cycle(Enum):
    Q1 = 45
    Q2 = 135
    Q3 = 225
    Q4 = 320

def load_df(url):
    parse_dates = ["Contract Starting Date", "Contract Ending Date"]
    df = pd.read_csv(url, parse_dates=parse_dates)
    # df.info()
    return df

print(load_df(URL))

def query_date_and_send_emails(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():

        contract_start_date = row["Contract Starting Date"].date()
        contract_start_date_work = contract_start_date
        contract_end_date = row["Contract Ending Date"].date()

        customer_name = row["CUSTOMER NAME"]
        email = row["Email ID"]
        amc_duration = row["DURATION in Months"]

        # mail info
        subject=''
        # due_date=row["due_date"].strftime("%d, %b %Y"), # example: 11, Aug 2024
        # amount=row["amount"] #TBD



        if (amc_duration == 24 and (contract_end_date - present) > 365):
            contract_start_date_work = contract_start_date + 365

        # #### PM REMINDERS ### (if under the AMC of 12/24 months)
        print(f'Present: {present}')
        print(f'contract_end_date: {contract_end_date}')

        
        if (present < contract_end_date):
            print(f"Entered check 1")

            subject=f'[ZIGMA Tech] Preventive Maintenance Reminder'

            print(f"start date + 45 days = {contract_start_date_work + timedelta(days=Cycle.Q1.value)}")
            if (present == contract_start_date_work + timedelta(days=Cycle.Q1.value)):
                # send mail of Q1
                print(f"Sending email")
                try:
                    send_email_for_pm(
                        subject=subject,
                        quarter=Cycle.Q1.name,
                        receiver_email=email,
                        name=customer_name,
                        due_date=contract_start_date_work + timedelta(days=Cycle.Q1.value + 45)
                    )
                    print(f"Email sent successfully to {email}!")
                except Exception as ex:
                    print(ex)
                continue

            if (present == contract_start_date_work + timedelta(days=Cycle.Q2.value)):
                # send mail of Q2
                print(f"Sending email")
                try:
                    send_email_for_pm(
                        subject=subject,
                        quarter=Cycle.Q2.name,
                        receiver_email=email,
                        name=customer_name,
                        due_date=contract_start_date_work + timedelta(days=Cycle.Q2.value + 45)
                    )
                    print(f"Email sent successfully!")
                except Exception as ex:
                    print(ex)
                continue

            if (present == contract_start_date_work + timedelta(days=Cycle.Q3.value)):
                # send mail of Q3
                print(f"Sending email")
                try:
                    send_email_for_pm(
                        subject=subject,
                        quarter=Cycle.Q3.name,
                        receiver_email=email,
                        name=customer_name,
                        due_date=contract_start_date_work + Cycle.Q3.value + 45
                    )
                    print(f"Email sent successfully!")
                except Exception as ex:
                    print(ex)
                continue

            if (present == contract_start_date_work + timedelta(days=Cycle.Q4.value)):
                # send mail of Q4
                print(f"Sending email")
                try:
                    send_email_for_pm(
                        subject=subject,
                        quarter=Cycle.Q4.name,
                        receiver_email=email,
                        name=customer_name,
                        due_date=contract_start_date_work + Cycle.Q4.value + 45
                    )
                    print(f"Email sent successfully!")
                except Exception as ex:
                    print(ex)
                continue
            
            print(f"present + timedelta(days=25) = {present + timedelta(days=25)}")
            if (contract_end_date == present + timedelta(days=25)):
                print(f"Sending email for AMC")
                try:
                    send_email_for_amc(
                        subject=subject,
                        receiver_email=email,
                        name=customer_name,
                        due_date=contract_end_date
                    )
                    print(f"Email sent successfully!")
                except Exception as ex:
                    print(ex)
                continue

        else:
            #### AMC RENEWAL ###
            subject=f'[ZIGMA Tech] AMC Renewal Reminder'

            if (amc_duration == 12):
                # send mail for AMC renewal
                pass
            elif (amc_duration == 24):
                # send mail for AMC renewal
                pass




        # if reminder date is today or already passed AND customer did not pay yet then, send reminder.
        # if (present >= row["reminder_date"].date()+15 and row["has_paid"] == "no"):
        #     send_email(
        #         subject=f'[Swarup Codes Pvt Ltd.] Invoice: {row["invoice_no"]}',
        #         name=row["name"],
        #         receiver_email=row["email"],
        #         due_date=row["due_date"].strftime("%d, %b %Y"), # example: 11, Aug 2024
        #         invoice_no=row["invoice_no"],
        #         amount=row["amount"]
        #     )
        #     email_counter += 1
    return f"Total email sent: {email_counter}"


if __name__ == "__main__":
    df = load_df(URL)
    result = query_date_and_send_emails(df)
    print(result)
