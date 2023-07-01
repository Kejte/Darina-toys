from django.db import models
from darinatoys.settings import MEDIA_URL

def upload_to_toys(instance, filename):
    return f"toys/{instance.toy.category.slug}/{instance.toy.slug}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя', null=False)
    slug = models.SlugField(verbose_name='Ярлык для URL', null=False, default='')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория игрушек'
        verbose_name_plural = 'Категории игрушек'
        ordering = ['name']

class Toy(models.Model):
    title = models.CharField(max_length=255, verbose_name='Имя', null=False)
    description = models.TextField(verbose_name='Описание', null=False)
    cost = models.IntegerField(verbose_name='Цена', null=False)
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', null=False)
    slug = models.SlugField(verbose_name='Ярлык для URL', null=False, default='', unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Игрушка'
        verbose_name_plural = 'Игрушки'
        ordering = ['is_published','category']

class Avatar(models.Model):
    photo = models.ImageField("Фото игрушки", upload_to=upload_to_toys, null=True)
    toy = models.ForeignKey(Toy, verbose_name="Связь к игрушке", on_delete=models.CASCADE, related_name="photos", null=True)

    def __str__(self) -> str:
        return f"Аватар для {self.toy}"


    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'

class CartItem(models.Model):
    toy = models.ForeignKey(Toy, verbose_name='Игрушка', null=False, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Количество', null=False, default=1)

class Cart(models.Model):
    items = models.ManyToManyField(CartItem, verbose_name='Игрушки', related_name='cart')
    user = models.OneToOneField('auth.User', verbose_name='Владелец корзины', null=False, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'Корзина пользователя {self.user.username}'
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class Transaction(models.Model):
    TRANSACTION_CHOICES=[
   ("NW", "Новый"),
   ("IN", "В обработке"),
   ("RD", "Готов"),
]
    items = models.ManyToManyField(CartItem, verbose_name='Игрушки', related_name='transaction')
    user = models.ForeignKey('auth.User', verbose_name='Владелец корзины',  null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=TRANSACTION_CHOICES, verbose_name='Статус заказа', null=False, default='NW')

    def __str__(self) -> str:
        return f'Транзакции пользователя {self.user.username}'
    
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
