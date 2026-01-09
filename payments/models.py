from django.db import models


class Item(models.Model):
    """Модель товара"""
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='usd',
        verbose_name='Валюта'
    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self):
        return self.name


class Discount(models.Model):
    """Модель скидки"""
    name = models.CharField(max_length=200, verbose_name='Название')
    percent_off = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name='Процент скидки'
    )
    stripe_coupon_id = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='Stripe Coupon ID'
    )
    
    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
    
    def __str__(self):
        return f"{self.name} ({self.percent_off}%)"


class Tax(models.Model):
    """Модель налога"""
    name = models.CharField(max_length=200, verbose_name='Название')
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name='Процент налога'
    )
    stripe_tax_rate_id = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='Stripe Tax Rate ID'
    )
    
    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'
    
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Order(models.Model):
    """Модель заказа"""
    items = models.ManyToManyField(Item, verbose_name='Товары')
    discount = models.ForeignKey(
        Discount, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Скидка'
    )
    tax = models.ForeignKey(
        Tax, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Налог'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ #{self.id}"
    
    def get_total_price(self):
        """Получить общую стоимость заказа"""
        total = sum(item.price for item in self.items.all())
        return total
    
    def get_currency(self):
        """Получить валюту заказа (берется из первого товара)"""
        first_item = self.items.first()
        return first_item.currency if first_item else 'usd'
