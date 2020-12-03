from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listingid>/", views.listing, name="listing"),
    path("category/<str:category>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("createsubmit",views.createsubmit,name="submit"),
    path("watchlist/<str:username>",views.watchlist,name="watchlist"),
    path("addwatchlist/<int:listingid>",views.addwatchlist,name="addwatchlist"),
    path("removewatchlist/<int:listingid>",views.removewatchlist,name="removewatchlist"),
    path("closebid/<int:listingid>", views.closebid, name="closebid"),
    path("bidsubmit/<int:listingid>", views.bidsubmit, name="bidsubmit"),
    path("cmntsubmit/<int:listingid>", views.cmntsubmit, name="cmntsubmit"),
    path("winnings", views.winnings, name="winnings")
]
