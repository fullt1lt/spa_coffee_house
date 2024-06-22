from django.urls import include, path
from django.contrib.auth.views import LogoutView
from myspa.views import (AdminMainPage, BlogNewsView, CafeTypeProductListView, CafeView, CreateMassageTherapistView, GalleryView, GetReviews, MainPage, Register, TypeBlogNewsViewListView, TypeCategoriesListView, TypeGalleryListView)


urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('main/', AdminMainPage.as_view(), name='main'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),
    path('create-massage-therapist/', CreateMassageTherapistView.as_view(), name='create_massage_therapist'),
    path('spa_category/<int:pk>/type_categories/', TypeCategoriesListView.as_view(), name='categories'),
    path('get_reviews/', GetReviews.as_view(), name='get_reviews'),
    path('cafe/', CafeView.as_view(), name='cafe'),
    path('cafe-categories/<int:pk>/type-product/', CafeTypeProductListView.as_view(), name='cafe_categories'),
    path('blog-news/', BlogNewsView.as_view(), name='blog_news'),
    path('blog-news-categories/<int:pk>/type-blog-news/', TypeBlogNewsViewListView.as_view(), name='blog_news_categories'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('gallery-categories/<int:pk>/type-gallery/', TypeGalleryListView.as_view(), name='gallery_categories'),
]