from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path('wishlist/<int:listing_id>/add', views.add_wishlist, name="add_wishlist"),
    path('wishlist/<int:listing_id>/remove', views.remove_wishlist, name="remove_wishlist"),
    path('bid/<int:listing_id>/', views.bid, name='bid'),
    path('close_listing/<int:listing_id>/', views.close_listing, name='close_listing'),
    path('comment/<int:listing_id>/', views.comment, name='comment'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('categories/', views.categories, name='categories'),
    path('category_listing/<str:category>', views.category_listing, name='category_listing'),
]
