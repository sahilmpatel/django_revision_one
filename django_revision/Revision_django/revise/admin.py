from django.contrib import admin
from .models import PersonDetails,Experiment,Customer,Vehicle,Accounts,Banks
# Register your models here.
admin.site.register(PersonDetails)
admin.site.register(Experiment)
admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Accounts)
admin.site.register(Banks)