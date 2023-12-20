from django.contrib.auth.models import User

ville = User.objects.create_user("ville", password="vallaton")
matti = User.objects.create_user("matti", password="meikäläinen")

ville.save()
matti.save()