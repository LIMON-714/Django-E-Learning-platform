from django.contrib import admin
from .models import TeamMember, Service, ServiceFeature, Review

# Register models
admin.site.register(TeamMember)
admin.site.register(Service)
admin.site.register(ServiceFeature)
admin.site.register(Review)
