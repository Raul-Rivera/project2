from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name ="index"),
    path("login", views.login_view, name ="login"),
    path("logout", views.logout_view, name ="logout"),
    path("register", views.register, name ="register"),
    path("item/new", views.new_item, name ="new_item" ),
    path("item/<int:id1>", views.item, name ="item"),
    path("bid/new/<int:id>", views.new_bid, name ="bid_new"),
    path("close/<int:id>", views.close_bid, name = "close_bid"),
    path("comment/new", views.comment, name = "comment"),
    path("watchlist/<int:id>/del", views.del_watch, name = "del_watch"),
    path("watchlist/<int:id>/new", views.new_watch, name = "new_watch"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("categories", views.categories, name = "categories"),
    path("category/<str:name>", views.cat_item, name = "cat_item")
]
