from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


CATEGORY_TIME = (
    (timedelta(minutes=30), "30"),
    (timedelta(minutes=60), "60"),
    (timedelta(minutes=90), "90"),
    (timedelta(minutes=120), "120"),
)

class SpaUser(AbstractUser):
    phone = models.CharField(max_length=16, blank=True, null=True) 
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    

class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    # categories = models.ForeignKey('SpaСategories', on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=20)
    type_categories = models.ManyToManyField('TypeCategories', related_name='type_categories')
    
    def __str__(self):
        return self.name

class MassageTherapist(models.Model):
    user = models.OneToOneField(SpaUser, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='therapists')
    position = models.ManyToManyField(Position, related_name='position')
    average_rating = models.FloatField(default=5.0)

    def save(self, *args, **kwargs):
        self.average_rating = round(self.average_rating, 1)
        super().save(*args, **kwargs)

    def __str__(self):
        positions = ', '.join([position.name for position in self.position.all()])
        return f"{self.user.username} - {positions}"
    
class Composition(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name} - {self.description[:40]}"

class SpaСategories(models.Model):
    name = models.CharField(max_length=100)
    categories_image = models.ImageField(upload_to='categories_image/', blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class TypeCategories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, related_name='composition')
    type_categories_image = models.ImageField(upload_to='type_categories_image/', blank=True, null=True)
    categories = models.ForeignKey(SpaСategories, on_delete=models.CASCADE, related_name='type_categories', default=1)
    
    def __str__(self):
        return self.name


class CategoriesSession(models.Model):
    type_category = models.ForeignKey(TypeCategories, on_delete=models.CASCADE, related_name='sessions')
    duration = models.DurationField(choices=CATEGORY_TIME)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type_category.name} - {self.get_duration_display()} - {self.price}"

    
class Day(models.Model):
    name = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.name


class TherapistAvailability(models.Model):
    therapist = models.ForeignKey(MassageTherapist, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.therapist.user.username} - {self.day.name} ({self.start_time} - {self.end_time})"


class Review(models.Model):
    user = models.ForeignKey(SpaUser, on_delete=models.CASCADE)
    therapist = models.ForeignKey(MassageTherapist, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_average_rating()

    def update_average_rating(self):
        therapist_reviews = self.therapist.reviews.all()
        total_rating = sum(review.rating for review in therapist_reviews)
        average_rating = total_rating / therapist_reviews.count()
        self.therapist.average_rating = average_rating
        self.therapist.save()

    def __str__(self):
        return f"{self.therapist} - {self.rating}"
    

# class Appointment(models.Model):
#     client = models.ForeignKey(SpaUser, on_delete=models.CASCADE)
#     therapist = models.ForeignKey(MassageTherapist, on_delete=models.CASCADE)
#     massage_type = models.ForeignKey(TypeCategories, on_delete=models.CASCADE)
#     date = models.DateField()
#     start_time = models.TimeField()
#     salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='appointments')

#     class Meta:
#         unique_together = ('therapist', 'date', 'start_time')

#     def __str__(self):
#         return f"{self.client.user.username} - {self.massage_type.name} with {self.therapist.user.username} on {self.date} at {self.start_time}"


    
class CafeProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='product_image/', blank=True, null=True)
    composition = models.TextField(max_length=250)
    type_cafe_product = models.ForeignKey("TypeCafeProduct", on_delete=models.CASCADE, related_name='type_categories', default=1)
    
    def __str__(self):
        return self.name
    

class TypeCafeProduct(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name