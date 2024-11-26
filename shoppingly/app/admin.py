from django.contrib import admin
from .models import(customer,
                    product,
                    cart,
                    orderplaced)

@admin.register(customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Name', 'Locality', 'City', 'Zipcode', 'State']
@admin.register(product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'Title', 'Selling_price', 'Discounted_price', 'Description','Brand', 'Category', 'Product_image']
@admin.register(cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'Product', 'Quantity']
@admin.register(orderplaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'customer', 'product','quantity', 'Order_date', 'order_status']