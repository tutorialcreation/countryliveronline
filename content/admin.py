from django.contrib import admin

from .models import Course, Video, Pricing, Subscription

admin.site.site_header = "country livers Admin"
admin.site.site_title = "country livers Admin Portal"
admin.site.index_title = "Welcome to the country livers Admin Portal"
admin.site.register(Course)
admin.site.register(Video)
admin.site.register(Pricing)
admin.site.register(Subscription)
