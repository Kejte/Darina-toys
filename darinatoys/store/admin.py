from django.contrib import admin
from .models import Toy, Category, Avatar, CartItem, Transaction, Cart

class AvatarInline(admin.TabularInline):
    fk_name = 'toy'
    model = Avatar
    verbose_name = 'Фото игрушки'
    verbose_name_plural = 'Настройка слайдера'

@admin.register(Toy)
class AdminToy(admin.ModelAdmin):
    list_display = ('title', 'category', 'cost', 'is_published', )
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AvatarInline,]
    list_filter = ('category', 'is_published')

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Transaction)
class AdminTransaction(admin.ModelAdmin):
    search_fields = ('user',)
    readonly_fields = ('user', 'items')
    list_display = ('user', 'status')
    list_filter = ('user', 'status')


    