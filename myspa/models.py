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
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    # categories = models.ForeignKey('SpaСategories', on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=20)
    spa_categories = models.ManyToManyField('SpaСategories', related_name='positions')
    
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
        return f"{self.user.first_name} {self.user.last_name} - {positions}"
    
class SpaСategories(models.Model):
    name = models.CharField(max_length=100)
    categories_image = models.ImageField(upload_to='categories_image/', blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class TypeCategories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    type_categories_image = models.ImageField(upload_to='type_categories_image/', blank=True, null=True)
    categories = models.ForeignKey(SpaСategories, on_delete=models.CASCADE, related_name='type_categories', default=1)
    
    def __str__(self):
        return self.name


class Procedure(models.Model):
    type_category = models.ForeignKey(TypeCategories, on_delete=models.CASCADE, related_name='sessions')
    duration = models.DurationField(choices=CATEGORY_TIME)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type_category.name} - {self.get_duration_display()} - {self.price}"


class Schedule(models.Model):
    therapist = models.ForeignKey(MassageTherapist, on_delete=models.CASCADE)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.therapist.user.username} - {self.day.strftime('%Y-%m-%d')} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class Record(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    start_time = models.TimeField()
    client = models.ForeignKey(SpaUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Procedure duration: {self.procedure.duration}\n start time: {self.start_time}"


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
    

class BlogAndNews(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    main_image = models.ImageField(upload_to='blog_image/', blank=True, null=True)
    small_image = models.ImageField(upload_to='blog_image/', blank=True, null=True)
    
    type_blog_and_news = models.ForeignKey("TypeBlogAndNews", on_delete=models.CASCADE, related_name='type_blog_and_news', default=1)
    
    def __str__(self):
        return self.name
    

class TypeBlogAndNews(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Gallery(models.Model):
    gallery_image = models.ImageField(upload_to='gallery_image/', blank=True, null=True)
    type_gallery = models.ForeignKey("TypeGallery", on_delete=models.CASCADE, related_name='type_gallery', default=1)
    
    def __str__(self):
        return self.type_gallery.name


class TypeGallery(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name