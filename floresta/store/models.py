import uuid

from django.db import models
from django.utils.text import slugify
from custom_user.models import User
from unidecode import unidecode
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        name = instance.first_name  # Default to first_name if name is not provided during registration
        if hasattr(instance, 'name') and instance.name:
            name = instance.name
        Customer.objects.create(user=instance, email=instance.email, name=name)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    new = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    second_image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Product, self).save(*args, **kwargs)

    @staticmethod
    def get_image_url(primary_image, fallback_image):
        """
        Retrieves the URL of the specified primary image. If the primary image is not available,
        falls back to the URL of the specified fallback image. If both images are unavailable,
        an empty string is returned.

        Parameters:
        primary_image: The primary image object.
        fallback_image: The fallback image object.

        Returns:
        str: The URL of the primary or fallback image, or an empty string if both are unavailable.
        """

        try:
            url = primary_image.url
        except ValueError:
            try:
                url = fallback_image.url
            except ValueError:
                url = ''
        return url

    @property
    def image_url(self):
        """
        Retrieves the URL of the primary image.

        Returns:
        str: The URL of the primary or fallback image, or an empty string if both are unavailable.
        """

        return self.get_image_url(self.image, self.second_image)

    @property
    def second_image_url(self):
        """
        Retrieves the URL of the secondary image.

        Returns:
        str: The URL of the secondary or fallback image, or an empty string if both are unavailable.
        """

        return self.get_image_url(self.second_image, self.image)


class Shipper(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(f"Zamówienie ID: {self.id}")

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def get_total_price(self):
        total = self.shipper.price + self.get_cart_total
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.order)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    postal_code = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=9, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)
