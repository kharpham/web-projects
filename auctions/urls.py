from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("closed_listing/", views.closed_listing, name="closed_listing"),
    path("all_listing/", views.all_listing, name="all_listing"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>", views.categories_listing, name="categories_listing"),
    path("view_listing/<int:listing_id>/", views.view_listing, name="view_listing"),
    path("view_listing/<int:listing_id>/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("view_listing/<int:listing_id>/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("view_listing/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("view_listing/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("watchlist/", views.watchlist_view, name="watchlist_view"),

]
