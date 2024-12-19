from django.contrib import admin
from .models import Category, ValidAnswer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ValidAnswer)
class ValidAnswerAdmin(admin.ModelAdmin):
    list_display = ('word', 'category')
    search_fields = ('word', 'category__name')