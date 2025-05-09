from django.db import models

class FriedItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    imgurl = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.price}฿"

class Order(models.Model):
    guest_name = models.CharField(max_length=100, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def __str__(self):
        if self.guest_name:
            return f"{self.id} - {self.guest_name}"
        return f"{self.id}"

class Flavor(models.Model):
    flavor_name = models.CharField(max_length=50)

    def __str__(self):
        return self.flavor_name
    
class Size(models.Model):
    size_name = models.CharField(max_length=10)
    charge = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.size_name} (+{self.charge})"

def get_default_size():
    return Size.objects.get(size_name='S').id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    fried = models.ForeignKey(FriedItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    size = models.ForeignKey(Size, on_delete=models.PROTECT, null=False, default=get_default_size)
    flavors = models.ManyToManyField(Flavor, blank=True)

    def get_total_price(self):
        base = self.fried.price
        charge = self.size.charge if self.size else 0

        flavor_count = self.flavors.count()
        extra_flavor_chare = max(0, flavor_count - 1) * 5
        return (base + charge + extra_flavor_chare) * self.quantity
    
    # def __str__(self):
    #     return f"{self.quantity} x {self.fried.name} by {self.order.id}"
    def __str__(self):
        if not self.pk:
            return f"{self.quantity} x {self.fried.name} ({self.size}) [unsaved flavors]"
    
        all_flavors = [f.flavor_name for f in self.flavors.all()]
        if len(all_flavors) > 3:
            shown = all_flavors[:3]  # โชว์แค่ 3 อัน
            flavors_str = ', '.join(shown) + '...'
        elif len(all_flavors) == 0:
            flavors_str = 'no flavor'
        else:
            flavors_str = ', '.join(all_flavors)

        return f"{self.quantity} x {self.fried.name} ({self.size.size_name}) [{flavors_str}] {self.get_total_price()}"
