import csv
import dateutil.parser as dparser
from dateutil.relativedelta import relativedelta as rd

rates = {"LONDON": 0.1,
         "PARIS": 0.12,
         "PORTO": 0.09}

reservations = []

with open("reservations.csv", "r") as f:
    reader = csv.DictReader(f, delimiter=',', quotechar='"')
    for row in reader:
        reservations.append(row)


# calculate the total commission GR receives from all reservations
def total_commission():
    total_commission = 0
    for reservation in reservations:
        if reservation['City'].upper() in rates.keys():
            total_commission += float(reservation["Net income, EUR"]) * \
                rates[reservation['City'].upper()]
        else:
            print(f"No rate for city {reservation['City']}")
    return total_commission


# commission per month
# should return {'05/2021': 1200} (example)
# are the commissions dependent on the ammount of time in a checkin? if not it's this, otherwise we would need to check
# how many days in each month
def commission_per_month():
    commission_dict = dict()
    for reservation in reservations:
        # if the format is always as is shown in the file than it makes sense to split instead of parsing with dateutil
        checkin_date = dparser.parse(reservation['Checkin'])  # .split("-")
        checkout_date = dparser.parse(reservation['Checkout'])  # .split("-")
        total_commission = 0

        if reservation['City'].upper() in rates.keys():
            total_commission += float(reservation["Net income, EUR"]) * \
                rates[reservation['City'].upper()]
        else:
            print(f"No rate for city {reservation['City']}")
            continue

        year_diff = checkout_date.year - checkin_date.year
        # 05/05/2020 -> 05/04/2021 -> 12 months
        year_to_month_diff = year_diff * 12
        month_diff = checkout_date.month - checkin_date.month

        monthly_rate = total_commission / (year_to_month_diff + month_diff + 1)
        current_date = checkin_date
        for i in range(year_to_month_diff + month_diff + 1):
            date_key = f"{checkout_date.month}/{checkout_date.year}"
            if not date_key in commission_dict.keys():
                commission_dict[date_key] = 0
            commission_dict[date_key] += monthly_rate
            current_date += rd(months=1)

    return commission_dict


def commission_by_city(city):
    city = city.upper()
    total_commission = 0
    for reservation in reservations:
        reservation_city = reservation['City'].upper()
        if (city == reservation_city) and (reservation_city in rates.keys()):
            total_commission += float(reservation["Net income, EUR"]
                                      ) * rates[reservation_city]
    if total_commission == 0:
        print("There are no current reservations in that city")
    return total_commission


if __name__ == '__main__':
    print(total_commission())
    print(commission_per_month())
    print(commission_by_city("paris"))
