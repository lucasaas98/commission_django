from django.shortcuts import render
from django.http import HttpResponse
from .models import City, Reservation
import csv
import dateutil.parser as dparser
from dateutil.relativedelta import relativedelta as rd


# Create your views here.
def index(request):
    return render(request, 'rate/index.html', {'reservations': Reservation.objects.all()})


def upload(request):
    data = {}
    if not request.POST:
        return render(request, 'rate/upload_reservations.html')
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            # messages.error(request,'File is not CSV type')
            return render(request, 'rate/upload_reservations.html', {
                'error_message': "That file is not in CSV format",
            })

        f = open("res.csv", "w")
        file_data = csv_file.read().decode("utf-8")
        f.write(file_data)
        f.close()

        all_reservations = []

        cities = City.objects.all()

        if len(cities) == 0:
            create_cities()

        reader = csv.DictReader(open("res.csv", "r"),
                                delimiter=',', quotechar='"')
        for row in reader:
            reservation, created = Reservation.objects.get_or_create(
                reservation=row['Reservation'],
                checkin_date=dparser.parse(row['Checkin']),
                checkout_date=dparser.parse(row['Checkout']),
                flat=row['Flat'],
                income=row["Net income, EUR"],
                city=[x for x in cities if x.city_name ==
                      row["City"].upper()][0]
            )
            all_reservations.append(reservation)
    except Exception as e:
        return render(request, 'rate/upload_reservations.html', {
            'error_message': "Error reading that file",
        })

    return render(request, 'rate/index.html', {'reservations': all_reservations})


def calculate_total(request):
    reservations = Reservation.objects.all()
    return render(request, 'rate/index.html', {'reservations': reservations, "function_result": total_commission(reservations)})


def calculate_monthly(request):
    reservations = Reservation.objects.all()
    return render(request, 'rate/index.html', {'reservations': reservations, "function_result": monthly_commission(reservations)})


def calculate_city(request):
    city_name = request.POST['city'].upper()
    reservations = Reservation.objects.all()
    return render(request, 'rate/index.html', {'reservations': reservations, "function_result": city_commissions(reservations, city_name)})


def total_commission(reservations):
    total_commission = 0
    for reservation in reservations:
        total_commission += reservation.income * reservation.city.rate
    return total_commission

# This version would be applied if you consider the income is divided by the months that encompass checkin date to checkout date 
# AKA this version does not consider how many days of a month are between checkin and checkout date
def monthly_commission_old(reservations):
    commission_dict = dict()
    for reservation in reservations:
        # if the format is always as is shown in the file than it makes sense to split instead of parsing with dateutil
        checkin_date = reservation.checkin_date # dparser.parse(reservation['Checkin'])  # .split("-")
        checkout_date =reservation.checkout_date # dparser.parse(reservation['Checkout'])  # .split("-")
        total_commission = 0

        total_commission += reservation.income * reservation.city.rate

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


def monthly_commission(reservations):
    commission_dict = dict()
    for reservation in reservations:
        checkin_date = reservation.checkin_date
        checkout_date =reservation.checkout_date
        total_commission = 0

        total_commission += reservation.income * reservation.city.rate

        delta = checkout_date - checkin_date

        daily_rate = total_commission / delta.days
        current_date = checkin_date
        for i in range(delta.days):
            date_key = f"{checkout_date.month}/{checkout_date.year}"
            if not date_key in commission_dict.keys():
                commission_dict[date_key] = 0
            commission_dict[date_key] += daily_rate
            current_date += rd(days=1)
    
    return commission_dict


def city_commissions(reservations, city_name):
    total_commission = 0
    for reservation in reservations:
        if reservation.city.city_name == city_name:
            total_commission += reservation.income * reservation.city.rate
    return total_commission


def create_cities():
    rates = {"LONDON": 0.1,
             "PARIS": 0.12,
             "PORTO": 0.09}
    for city_name, rate in rates.items():
        obj, created = City.objects.get_or_create(
            city_name=city_name, rate=rate)
