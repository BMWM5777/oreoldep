from django.contrib import admin
from .models import Auction, Bid, AuctionImage
from django.contrib import messages

class AuctionImageInline(admin.TabularInline):
    model = AuctionImage
    extra = 1

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    inlines = [AuctionImageInline]
    list_display = (
        'title', 
        'seller', 
        'winner_display',
        'status', 
        'auction_type', 
        'created_at'
    )
    list_filter = ('status', 'auction_type')
    search_fields = ('title', 'seller__username', 'winner__username')
    actions = ['approve_auctions', 'reject_auctions']

    def winner_display(self, obj):
        """Отображение имени победителя, если есть."""
        return obj.winner.username if obj.winner else "Нет победителя"
    winner_display.short_description = "Победитель"

    def approve_auctions(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"Подтверждено {updated} лотов.", messages.SUCCESS)
    approve_auctions.short_description = "Подтвердить выбранные лоты"

    def reject_auctions(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"Отклонено {updated} лотов.", messages.ERROR)
    reject_auctions.short_description = "Отклонить выбранные лоты"

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'bidder', 'bid_amount', 'timestamp')
    list_filter = ('auction',)
    search_fields = ('auction__title', 'bidder__username')
