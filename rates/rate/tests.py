from django.test import TestCase
from .models import City, Reservation
from .views import total_commission, monthly_commission, city_commissions
import datetime


class ModelsTestCase(TestCase):
    def test_city_has_name(self):
        city = City.objects.create(city_name="TheName")
        city.rate = 0.10
        city.save()
        self.assertEqual(city.city_name, "TheName")

    def test_city_has_rate(self):
        city = City.objects.create(rate=0.10)
        city.city_name = "TheName"
        city.save()
        self.assertEqual(city.rate, 0.10)

    def test_reservation_has_all_data(self):
        city = City.objects.create(city_name="TheName", rate=0.10)
        city.save()

        checkin = datetime.datetime.fromtimestamp(1623849246)
        checkout = datetime.datetime.fromtimestamp(1626441246)
        reservation = Reservation.objects.create(
            reservation='HM123',
            checkin_date=checkin,
            checkout_date=checkout,
            flat='Flat',
            income=1900,
            city=city
        )
        reservation.save()

        self.assertEqual(reservation.reservation, 'HM123')
        self.assertEqual(reservation.checkin_date, checkin)
        self.assertEqual(reservation.checkout_date, checkout)
        self.assertEqual(reservation.flat, 'Flat')
        self.assertEqual(reservation.income, 1900)
        self.assertEqual(reservation.city.city_name, "TheName")
        self.assertEqual(reservation.city.rate, 0.10)

    def test_total_commission(self):
        city1 = City.objects.create(city_name="TheName", rate=0.10)
        city1.save()

        city2 = City.objects.create(city_name="TheName2", rate=0.20)
        city2.save()

        checkin = datetime.datetime.fromtimestamp(1623849246)
        checkout = datetime.datetime.fromtimestamp(1626441246)
        reservation1 = Reservation.objects.create(
            reservation='HM123',
            checkin_date=checkin,
            checkout_date=checkout,
            flat='Flat',
            income=1000,
            city=city1
        )
        reservation1.save()
        
        reservation2 = Reservation.objects.create(
            reservation='HM124',
            checkin_date=checkin,
            checkout_date=checkout,
            flat='Flat1',
            income=1000,
            city=city2
        )
        reservation2.save()

        reservations = [reservation1, reservation2]
        self.assertEquals(total_commission(reservations), 0.1*1000+0.2*1000)

    def test_city_commission(self):
        city1 = City.objects.create(city_name="THENAME", rate=0.10)
        city1.save()

        checkin = datetime.datetime.fromtimestamp(1623849246)
        checkout = datetime.datetime.fromtimestamp(1626441246)
        reservation1 = Reservation.objects.create(
            reservation='HM123',
            checkin_date=checkin,
            checkout_date=checkout,
            flat='Flat',
            income=700,
            city=city1
        )
        reservation1.save()
        
        reservation2 = Reservation.objects.create(
            reservation='HM124',
            checkin_date=checkin,
            checkout_date=checkout,
            flat='Flat1',
            income=900,
            city=city1
        )
        reservation2.save()

        reservations = [reservation1, reservation2]
        self.assertEquals(city_commissions(reservations, "THENAME"), 0.1*700+0.1*900)

    def test_monthly_commission(self):
        city1 = City.objects.create(city_name="THENAME", rate=0.10)
        city1.save()

        checkin = datetime.datetime.fromtimestamp(1623849246)
        checkout = datetime.datetime.fromtimestamp(1626441246)
        reservation1 = Reservation.objects.create(
            reservation='HM123',
            checkin_date=checkin,
            checkout_date=checkout,
            flat='Flat',
            income=700,
            city=city1
        )
        reservation1.save()
        
        checkout2 = datetime.datetime.fromtimestamp(1624194846)
        reservation2 = Reservation.objects.create(
            reservation='HM124',
            checkin_date=checkin,
            checkout_date=checkout2,
            flat='Flat1',
            income=900,
            city=city1
        )
        reservation2.save()

        reservations = [reservation1, reservation2]
        self.assertEquals(monthly_commission(reservations), {'7/2021': 70.0, '6/2021': 90.0})


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_upload_loads_properly(self):
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)

    def test_random_loads_404(self):
        response = self.client.get('/randomurl')
        self.assertEqual(response.status_code, 404)
