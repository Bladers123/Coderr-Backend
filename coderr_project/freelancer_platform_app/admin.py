from django.contrib import admin
from .models import Offer, Order, Profile, BaseInfo, Review, FileUpload, OfferDetail



admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(BaseInfo)
admin.site.register(Review)
admin.site.register(FileUpload)
admin.site.register(OfferDetail)


