from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'rating', 'created_at')
    search_fields = ('text',)
    list_filter = ('rating', 'created_at')

