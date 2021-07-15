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
            total_commission += float(reservation["Net income, EUR"]) * rates[reservation['City']]
        else:
            print(f"No rate for city {reservation['City']}")
    return total_commission

# commission per month
# should return {'05/2021': 1200} (example)
# def commission_per_month():


# def commission_by_city(city):





if __name__ == '__main__':
    print(total_commission())
    # print(commission_by_city("london"))
    # print(commission_per_month())
    # print(data)
