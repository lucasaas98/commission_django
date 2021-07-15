import csv

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
            total_commission += float(reservation["Net income, EUR"]) * rates[reservation['City'].upper()]
        else:
            print(f"No rate for city {reservation['City']}")
    return total_commission

# commission per month
# should return {'05/2021': 1200} (example)
# def commission_per_month():


def commission_by_city(city):
    city = city.upper()
    total_commission = 0
    for reservation in reservations:
        reservation_city = reservation['City'].upper()
        if (city == reservation_city) and (reservation_city in rates.keys()):
            total_commission += float(reservation["Net income, EUR"]) * rates[reservation_city]
    if total_commission == 0:
        print("There are no current reservations in that city")
    return total_commission




if __name__ == '__main__':
    print(total_commission())
    print(commission_by_city("paris"))
    # print(commission_per_month())
    # print(data)
