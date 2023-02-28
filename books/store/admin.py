from django.contrib import admin
from store.models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')
    # list_display = __all__
    list_display_links = ('id',)
    # если один аргумент, то обязательно запятую, для получения кортежа
    # без запятой будет просто строка в круглых скобках
    search_fields = ('name', 'price')
    list_editable = ('name', 'price')
    list_filter = ('name','price')

admin.site.register(Book,BookAdmin)