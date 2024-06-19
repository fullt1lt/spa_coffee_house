from django.urls import include, path
from django.contrib.auth.views import LogoutView
from myspa.views import (BlogNewsView, CafeTypeProductListView, CafeView, CreateMassageTherapistView, GetReviews, Login, MainPage, Register, TypeBlogNewsViewListView, TypeCategoriesListView)


urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
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
]