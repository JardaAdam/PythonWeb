from django.core.validators import MinValueValidator
from django.db.models import CASCADE, IntegerField, DateTimeField, BooleanField
from django.db.models import Model, ForeignKey, DecimalField

from accounts.models import CustomUser
from revisions.models import TypeOfPpe


# Create your models here.
class CalculatorOutput(Model):
    customer = ForeignKey(CustomUser, related_name='orders', related_query_name='custom_order', default=None,
                          on_delete=CASCADE, null=False, blank=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    is_submitted = BooleanField(default=False)
    total_price = DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order by {self.customer.username} with total {self.total_price} Kč"

    def calculate_total(self):
        """ Metoda pro výpočet celkové ceny """
        total = 0
        for item in self.calculatoritems.all():
            total += item.type_of_ppe.price * item.quantity
        self.total_price = total
        self.save()

class CalculatorItem(Model):
    calculator = ForeignKey(CalculatorOutput, related_name='calculatoritems', on_delete=CASCADE)
    type_of_ppe = ForeignKey(TypeOfPpe, on_delete=CASCADE)
    quantity = IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.quantity} x {self.type_of_ppe.group_type_ppe}"
