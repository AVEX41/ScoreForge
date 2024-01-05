from django.contrib import admin
from .models import User, PerformanceIndicator, DataPoint


admin.site.register(User)
admin.site.register(PerformanceIndicator)
admin.site.register(DataPoint)
