from django.contrib import admin
from .models import Listing, Watchlist, Bid, User

# Register your models here.
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(User)
