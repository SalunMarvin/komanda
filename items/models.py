from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Color(models.Model):
    name = models.CharField(max_length=250, blank=False, default='')
    hex = models.CharField(max_length=6, blank=False, default='')

    class Meta:
        verbose_name = "Cor"
        verbose_name_plural = "Cores"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=250, blank=False, default='')
    description = models.CharField(max_length=250, blank=True)
    color = models.ForeignKey(Color, null=True, blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=250, blank=False, default='')
    description = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marca"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    slug = models.SlugField(null=False, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    active = models.BooleanField(default=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    barcode = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', null=True, blank=True)
    brand = models.ForeignKey(Brand, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, null=False)
    number = models.BigIntegerField(null=True, blank=True, unique=False)
    products = models.ManyToManyField(Product, through='Quantity', blank=True)
    finalPrice = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    partialPaid = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    createdAt = models.DateTimeField(auto_now=True, null=True)
    isFinished = models.BooleanField(default=False)
    documentNumber = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Comanda"
        verbose_name_plural = "Comandas"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  # set the slug explicitly
        super(Ticket, self).save(*args, **kwargs)  # call Django's save()

    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.number)


class Quantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Quantidade"
        verbose_name_plural = "Quantidades"

    def __str__(self):
        return str(self.quantity)
