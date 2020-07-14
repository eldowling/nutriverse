from django.db import models


class Category(models.Model):

    code = models.CharField(max_length=254)
    name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.code

    def get_name(self):
        return self.name

class Subcategory(models.Model):

    code = models.CharField(max_length=254)
    name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.code

    def get_name(self):
        return self.name

class Subscription_Type(models.Model):

    code = models.CharField(max_length=254)
    name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.code

    def get_name(self):
        return self.name


class Sizes(models.Model):

    code = models.CharField(max_length=254)
    name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.code

    def get_name(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    subcategory = models.ForeignKey('Subcategory', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    code = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    subscription = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    quantity_available = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    size = models.CharField(max_length=254, null=True, blank=True)
    colour = models.CharField(max_length=254, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product_Subscription(models.Model):

    code = models.CharField(max_length=254)
    product = models.ForeignKey('Product', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    subscription_type = models.ForeignKey('Subscription_Type', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    quantity_available = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)

    def __str__(self):
        return self.code

    def get_name(self):
        return self.name