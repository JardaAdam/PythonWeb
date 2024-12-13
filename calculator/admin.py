from django.contrib import admin

from .models import CalculatorOrder, CalculatorItem
# Register your models here.
admin.site.register(CalculatorOrder)
admin.site.register(CalculatorItem)