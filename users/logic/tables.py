import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Restaurant.settings')
django.setup()

from users.models import Table

table1 = Table(number=1, capacity=2)
table1.save()

table2 = Table(number=2, capacity=2)
table2.save()

table3 = Table(number=3, capacity=2)
table3.save()

table4 = Table(number=4, capacity=2)
table4.save()

table5 = Table(number=5, capacity=2)
table5.save()

table6 = Table(number=6, capacity=2)
table6.save()

table7 = Table(number=7, capacity=1)
table7.save()

table8 = Table(number=8, capacity=1)
table8.save()

table9 = Table(number=9, capacity=1)
table9.save()

table10 = Table(number=10, capacity=1)
table10.save()


table11 = Table(number=11, capacity=1)
table11.save()

table12 = Table(number=12, capacity=4)
table12.save()

table13 = Table(number=13, capacity=4)
table13.save()

table14 = Table(number=14, capacity=4)
table14.save()

table15 = Table(number=15, capacity=2)
table15.save()

table16 = Table(number=16, capacity=2)
table16.save()

table17 = Table(number=17, capacity=4)
table17.save()

table18 = Table(number=18, capacity=2)
table18.save()

table19 = Table(number=19, capacity=4)
table19.save()

table20 = Table(number=20, capacity=2)
table20.save()

table21 = Table(number=21, capacity=5)
table1.save()

table22 = Table(number=22, capacity=6)
table22.save()

table23 = Table(number=23, capacity=6)
table23.save()

table24 = Table(number=24, capacity=2)
table24.save()

table25 = Table(number=25, capacity=2)
table25.save()

table26 = Table(number=26, capacity=4)
table26.save()

table27 = Table(number=27, capacity=4)
table27.save()
