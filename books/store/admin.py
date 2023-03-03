from django.contrib.admin import ModelAdmin
from django.contrib import admin
from store.models import Book, UserBookRelation

class BookAdmin(ModelAdmin):
    # list_display = ('id','name','price')
    list_display = [field.name for field in Book._meta.get_fields()]
    # list_display = __all__
    list_display_links = ('id',)
    # если один аргумент, то обязательно запятую, для получения кортежа
    # без запятой будет просто строка в круглых скобках
    search_fields = ('name', 'price')
    # list_editable = ('name', 'price')
    list_filter = ('name','price')
    list_editable = [field.name for field in Book._meta.fields if field.name != "id"]

admin.site.register(Book,BookAdmin)

@admin.register(UserBookRelation)
class UserBookRelation(ModelAdmin):
    pass