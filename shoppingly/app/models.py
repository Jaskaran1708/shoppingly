from django.db import models
from django.contrib.auth.models import User
State_choices =  (("Andhra Pradesh","Andhra Pradesh"),
                 ("Arunachal Pradesh ","Arunachal Pradesh "),
                 ("Assam","Assam"),("Bihar","Bihar"),
                 ("Chhattisgarh","Chhattisgarh"),
                 ("Goa","Goa"),("Gujarat","Gujarat"),
                 ("Haryana","Haryana"),
                 ("Himachal Pradesh","Himachal Pradesh"),
                 ("Jammu and Kashmir ","Jammu and Kashmir "),
                 ("Jharkhand","Jharkhand"),
                 ("Karnataka","Karnataka"),
                 ("Kerala","Kerala"),
                 ("Madhya Pradesh","Madhya Pradesh"),
                 ("Maharashtra","Maharashtra"),
                 ("Manipur","Manipur"),
                 ("Meghalaya","Meghalaya"),
                 ("Mizoram","Mizoram"),
                 ("Nagaland","Nagaland"),
                 ("Odisha","Odisha"),
                 ("Punjab","Punjab"),
                 ("Rajasthan","Rajasthan"),
                 ("Sikkim","Sikkim"),
                 ("Tamil Nadu","Tamil Nadu"),
                 ("Telangana","Telangana"),
                 ("Tripura","Tripura"),
                 ("Uttar Pradesh","Uttar Pradesh"),
                 ("Uttarakhand","Uttarakhand"),
                 ("West Bengal","West Bengal"),
                 ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
                 ("Chandigarh","Chandigarh"),
                 ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
                 ("Daman and Diu","Daman and Diu"),
                 ("Lakshadweep","Lakshadweep"),
                 ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
                 ("Puducherry","Puducherry"),
                 ('Raman','Rraman'))
class customer(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    Name = models.CharField(max_length=50, null=False)
    Locality = models.CharField(max_length=100,  null=False)
    City = models.CharField(max_length=50)
    Zipcode = models.IntegerField()
    State = models.CharField(choices = State_choices, max_length=50)

    def __str__(self):
        return str(self.id)

Category_Choices = (
            ('M', 'Mobile'),
            ('L', 'Laptop'),
            ('TW', 'Top Wear'),
            ('BW', 'Bottom Wear'),
           )
class product(models.Model):
    Title = models.CharField( max_length=50)
    Selling_price = models.IntegerField()
    Discounted_price = models.IntegerField()
    Description = models.TextField(max_length=50)
    Brand = models.CharField(max_length=50)
    Category = models.CharField(choices = Category_Choices, max_length=2)
    Product_image = models.ImageField( upload_to= 'Productimg')

    def __str__(self):
        return str(self.id)
    
class cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    Product = models.ForeignKey(product, on_delete= models.CASCADE)
    Quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.Quantity * self.Product.Discounted_price
    @property
    def cart_counter(self):
        return self.Product.count()
Status_choice = (('Pending', 'Pending'),
                 ('Accepted', 'Accepted'),
                 ('Packed', 'Packed'),
                 ('On the way', 'On the way'),
                 ('Delivered', 'Delivered'),
                 ('Cancel', 'Cancel'),
                 )
class orderplaced(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(product, on_delete = models.CASCADE)
    customer = models.ForeignKey(customer,on_delete = models.CASCADE)
    order_status = models.CharField( max_length=50, choices = Status_choice, default = 'pending')
    quantity = models.PositiveIntegerField(default = 1)
    Order_date = models.DateField(auto_now_add = True)
    @property
    def total_cost(self):
        return self.quantity * self.product.Discounted_price

