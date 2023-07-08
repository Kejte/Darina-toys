from django.contrib import admin
from .models import Toy, Category, Avatar, Transaction, Cart, Review

class AvatarInline(admin.TabularInline):
    fk_name = 'toy'
    model = Avatar
    verbose_name = 'Фото игрушки'
    verbose_name_plural = 'Настройка слайдера'

class ReviewInline(admin.TabularInline):
    fk_name = 'toy'
    model = Review
    verbose_name = 'Отзыв о игрушке'
    verbose_name_plural = 'Отзывы об игрушке'
    readonly_fields = ('title', 'description', 'rating', 'toy', 'user')

@admin.register(Toy)
class AdminToy(admin.ModelAdmin):
    list_display = ('title', 'category', 'cost', 'is_published', )
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AvatarInline, ReviewInline]
    list_filter = ('category', 'is_published')

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Transaction)
class AdminTransaction(admin.ModelAdmin):
    search_fields = ('user',)
    readonly_fields = ('user', 'items')
    list_display = ('user', 'status')
    list_filter = ('user', 'status')


    