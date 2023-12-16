from django.contrib import admin
from .models import User, CompetitionType, Competition, CompetitionShot


admin.site.register(User)
admin.site.register(CompetitionType)
admin.site.register(Competition)
admin.site.register(CompetitionShot)
