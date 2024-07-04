from django.urls import include, path
from django.contrib.auth.views import LogoutView
from myspa.views import (AdminMainPage, BlogNewsView, CafeTypeProductListView, CafeView, DeleteSpaCategoriesView, DeleteTherapistView, GalleryView, GetReviews, MainPage, Register, TypeBlogNewsViewListView, TypeCategoriesListView, TypeGalleryListView, get_therapist_schedule)


urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),
    path('spa_category/<int:pk>/type_categories/', TypeCategoriesListView.as_view(), name='categories'),
    path('get_reviews/', GetReviews.as_view(), name='get_reviews'),
    path('cafe/', CafeView.as_view(), name='cafe'),
    path('cafe-categories/<int:pk>/type-product/', CafeTypeProductListView.as_view(), name='cafe_categories'),
    path('blog-news/', BlogNewsView.as_view(), name='blog_news'),
    path('blog-news-categories/<int:pk>/type-blog-news/', TypeBlogNewsViewListView.as_view(), name='blog_news_categories'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('gallery-categories/<int:pk>/type-gallery/', TypeGalleryListView.as_view(), name='gallery_categories'),
    path('category-delete/<int:pk>/', DeleteSpaCategoriesView.as_view(), name='category_delete'),
    path('therapist-delete/<int:pk>/', DeleteTherapistView.as_view(), name='therapist_delete'),
    path('schedule/<int:therapist_id>/', get_therapist_schedule, name='get_therapist_schedule'),
    path('admin-main-page/', AdminMainPage.as_view(), name='admin_main_page'),
]