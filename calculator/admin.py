from django.contrib import admin

from .models import CalculatorOutput, CalculatorItem
# Register your models here.
admin.site.register(CalculatorOutput)
admin.site.register(CalculatorItem)