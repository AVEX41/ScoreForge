from django.contrib import admin
from .models import User, ScoreTable, ScoreSet, ScoreNode


admin.site.register(User)
admin.site.register(ScoreTable)
admin.site.register(ScoreSet)
admin.site.register(ScoreNode)
