from django.core.validators import MinValueValidator

from django.db.models import CASCADE, IntegerField, DateTimeField, BooleanField, SET_NULL
from django.db.models import Model, ForeignKey, DecimalField

from accounts.models import CustomUser
from django.conf import settings
from revisions.models import TypeOfPpe

"""PPE = PersonalProtectiveEquipment"""
# Create your models here.

class CalculatorOrder(Model):
    """Tento model reprezentuje záznam objednávky
        - Obsahuje odkazy na uživatele (zákazníka) a sledování stavu objednávky.
        - Poskytuje prostředky pro výpočet celkové ceny revize.
    """
    customer = ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', related_query_name='custom_order', default=None,
                          on_delete=CASCADE, null=False, blank=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    is_submitted = BooleanField(default=False)
    total_price_revision = DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f"Order {self.id} by {self.customer.username} with total {self.total_price} Kč"

    def __repr__(self):
        return (f"CalculatorOrder(id={self.id}, "
                f"customer={self.customer.username}, "
                f"total_price={self.total_price}, "
                f"is_submitted={self.is_submitted})")


    def calculate_revision_total_price(self):
        """ Metoda pro výpočet celkové ceny """
        total = 0
        for item in self.calculatoritems.all():
            total += item.type_of_ppe.price * item.quantity
        self.total_price = total
        self.save()


class CalculatorItem(Model):
    """Tento model bude udržovat informace o jednotlivých položkách v objednávce
        - Modeluje jednotlivé položky v rámci objednávky `CalculatorOrder`.
        - Umožňuje uživatelům zadat množství pro každý typ položky, přičemž používá `MinValueValidator` pro zajištění, že množství je logické.
    """
    calculator_order = ForeignKey(CalculatorOrder, related_name='calculatoritems', on_delete=CASCADE)
    type_of_ppe = ForeignKey(TypeOfPpe, on_delete=SET_NULL, null=True)
    quantity = IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.type_of_ppe.group_type_ppe}"

    def __repr__(self):
        return (f"CalculatorItem(id={self.id}, "
                f"calculator_order_id={self.calculator_order.id}, "
                f"type_of_ppe={self.type_of_ppe.group_type_ppe if self.type_of_ppe else 'None'}, "
                f"quantity={self.quantity})")
