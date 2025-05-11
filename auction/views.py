from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Auction, Bid, AuctionImage
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import AuctionForm, BidForm, AuctionImageFormSet
from django.utils import timezone
from django.db.models import Count, Avg
from datetime import timedelta
import json
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db import transaction
from auction.templatetags.censor import censor_username
from utils.decorators import require_auth


@login_required
def create_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES)
        formset = AuctionImageFormSet(request.POST, request.FILES, queryset=AuctionImage.objects.none())

        if form.is_valid() and formset.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
            auction.current_price = auction.starting_price
            auction.status = "pending"
            auction.save()

            for image_form in formset:
                if image_form.cleaned_data.get('image') and not image_form.cleaned_data.get('DELETE'):
                    AuctionImage.objects.create(
                        auction=auction,
                        image=image_form.cleaned_data['image']
                    )
                    print("Добавлено изображение:", image_form.cleaned_data['image'])

            messages.success(request, "Ваш лот отправлен на модерацию.")
            return redirect('auction:list')

        else:
            messages.error(request, "Проверьте правильность введённых данных.")

    else:
        form = AuctionForm()
        formset = AuctionImageFormSet(queryset=AuctionImage.objects.none())

    return render(request, "auction/create_auction.html", {
        "form": form,
        "formset": formset
    })


@require_auth()
def auction_list(request):
    auctions = Auction.objects.filter(status='approved', end_time__gt=timezone.now()).order_by('-created_at')
    return render(request, "auction/auction_list.html", {"auctions": auctions})


@login_required
def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id, status='approved')

    import datetime
    can_bid = True
    inform_message = ""
    if timezone.now() < auction.start_time:
        inform_message = "Аукцион еще не начался. Ставки будут доступны после " + auction.start_time.strftime("%d.%m.%Y %H:%M")
        can_bid = False
    
    if auction.status == 'completed':
        messages.info(request, "Аукцион завершён.")
        form = None
    else:
        if request.method == "POST" and can_bid:
            form = BidForm(request.POST)
            if form.is_valid():
                bid_amount = form.cleaned_data['bid_amount']
                min_bid = auction.current_price + auction.bid_step
                if bid_amount < min_bid:
                    form.add_error('bid_amount', f'Минимальная ставка должна быть не меньше {min_bid} тенге.')
                else:
                    Bid.objects.create(
                        auction=auction,
                        bidder=request.user,
                        bid_amount=bid_amount
                    )
                    auction.current_price = bid_amount
                    auction.save()
                    return redirect('auction:detail', auction_id=auction.id)
        else:
            form = BidForm()
    
    bids = auction.bids.order_by('-timestamp')
    
    context = {
        "auction": auction,
        "bids": bids,
        "form": form,
        "inform_message": inform_message,
        "can_bid": can_bid,
    }
    return render(request, "auction/auction_detail.html", context)


@staff_member_required
def admin_dashboard(request):
    total_auctions = Auction.objects.count()
    approved_auctions = Auction.objects.filter(status='approved').count()
    pending_auctions = Auction.objects.filter(status='pending').count()
    rejected_auctions = Auction.objects.filter(status='rejected').count()
    completed_auctions = Auction.objects.filter(status='completed').count()
    change_requested_auctions = Auction.objects.filter(status='change_requested').count()
    pending_list = Auction.objects.filter(status='pending').order_by('-created_at')
    change_requested_list = Auction.objects.filter(status='change_requested').order_by('-created_at')
    
    avg_bid = Bid.objects.aggregate(average=Avg('bid_amount'))['average']

    if request.method == 'POST':
        auction_id = request.POST.get('auction_id')
        auction_obj = get_object_or_404(Auction, id=auction_id, status__in=['pending', 'change_requested'])
        if 'approve' in request.POST:
            auction_obj.status = 'approved'
            auction_obj.save()
            messages.success(request, f"Лот «{auction_obj.title}» подтверждён.")
        elif 'reject' in request.POST:
            auction_obj.status = 'rejected'
            auction_obj.save()
            messages.error(request, f"Лот «{auction_obj.title}» отклонён.")
        elif 'request_change' in request.POST:
            comment = request.POST.get('admin_comment', '')
            auction_obj.status = 'change_requested'
            auction_obj.admin_comment = comment
            auction_obj.save()
            messages.info(request, f"Запрос на изменение для лота «{auction_obj.title}» отправлен.")
        return redirect('auction:admin_dashboard')
    
    one_month_ago = timezone.now() - timedelta(days=30)
    auctions_last_month = Auction.objects.filter(created_at__gte=one_month_ago)
    auctions_by_day = auctions_last_month.extra({'day': "DATE(created_at)"}).values('day').annotate(count=Count('id')).order_by('day')
    days = []
    auctions_counts = []
    for item in auctions_by_day:
        day_str = item['day'] if isinstance(item['day'], str) else item['day'].strftime("%Y-%m-%d")
        days.append(day_str)
        auctions_counts.append(item['count'])
    
    status_data = {
        'approved': approved_auctions,
        'pending': pending_auctions,
        'rejected': rejected_auctions,
        'completed': completed_auctions,
        'change_requested': change_requested_auctions,
    }
    dashboard_data = {
        'days': days,
        'auctionsCounts': auctions_counts,
        'statusData': status_data,
    }
    context = {
        'total_auctions': total_auctions,
        'approved_auctions': approved_auctions,
        'pending_auctions': pending_auctions,
        'rejected_auctions': rejected_auctions,
        'completed_auctions': completed_auctions,
        'change_requested_auctions': change_requested_auctions,
        'avg_bid': avg_bid,
        'dashboard_data_json': json.dumps(dashboard_data),
        'pending_list': pending_list,
        'change_requested_list': change_requested_list,
    }
    return render(request, 'auction/admin_dashboard.html', context)


@staff_member_required
def auction_modal_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    html = render_to_string('auction/auction_modal_detail.html', {'auction': auction}, request=request)
    return JsonResponse({'html': html})


@login_required
def my_auctions(request):
    user_auctions = Auction.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'auction/my_auctions.html', {'auctions': user_auctions})


@login_required
def edit_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    if auction.seller != request.user:
        messages.error(request, "Вы не являетесь владельцем данного лота.")
        return redirect('auction:list')

    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES, instance=auction)
        formset = AuctionImageFormSet(request.POST, request.FILES, queryset=auction.images.all())

        if form.is_valid() and formset.is_valid():
            updated_auction = form.save(commit=False)
            updated_auction.status = 'change_requested'
            updated_auction.save()
            for image_form in formset:
                if image_form.cleaned_data and image_form.cleaned_data.get('image'):
                    image_obj = image_form.save(commit=False)
                    image_obj.auction = updated_auction
                    image_obj.save()
            messages.success(request, "Изменения сохранены и отправлены на проверку.")
            return redirect('auction:my_auctions')
        else:
            messages.error(request, "Исправьте ошибки в форме.")
    else:
        form = AuctionForm(instance=auction)
        formset = AuctionImageFormSet(queryset=auction.images.all())

    return render(request, 'auction/edit_auction.html', {
        'form': form,
        'formset': formset,
        'auction': auction,
    })


def get_bids(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    bids = auction.bids.order_by('-timestamp')
    bids_html = render_to_string('auction/_bids_list.html', {'bids': bids})
    return JsonResponse({'bids_html': bids_html})


def get_auction_status(request, auction_id):
    with transaction.atomic():
        auction = Auction.objects.select_for_update().get(id=auction_id)

        if auction.auction_type == 'live' and auction.status != 'completed':
            last_bid = auction.bids.order_by('-timestamp').first()
            if last_bid:
                bid_time = last_bid.timestamp
                if (auction.end_time - bid_time).total_seconds() < 15:
                    additional_time = timedelta(seconds=15)
                    auction.end_time = timezone.now() + additional_time
                    auction.save()

        if timezone.now() >= auction.end_time and auction.status != 'completed':
            last_bid = auction.bids.order_by('-timestamp').first()
            if last_bid:
                auction.winner = last_bid.bidder
            auction.status = 'completed'

            if auction.winner and not auction.notified:
                if auction.winner.email:
                    subject = f"Уведомление о победе в аукционе от СТО «Ореол»"
                    message = (
                        f"Уважаемый(ая) {auction.winner.username},\n\n"
                        f"Настоящим уведомляем Вас о том, что по результатам проведения аукциона Вы стали победителем лота: «{auction.title}».\n"
                        f"Ваша выигрышная ставка составила: {auction.current_price} тенге.\n\n"
                        "Просим Вас в ближайшее время связаться с представителем компании для уточнения условий передачи лота и оформления необходимых документов.\n\n"
                        "Контактная информация:\n"
                        "Телефон: +7 (778) 551-40-08\n"
                        "Электронная почта: oreol.kz@mail.ru\n"
                        "Веб-сайт: oreol.kz\n\n"
                        "Благодарим Вас за участие и доверие к нашей компании.\n\n"
                        "С уважением,\n"
                        "Администрация\n"
                        "ТОО «Ореол»"
                    )
                    send_mail(subject, message, None, [auction.winner.email])

                auction.notified = True

            auction.save()

    winner_censored = censor_username(auction.winner.username) if auction.winner else None
    
    is_current_user_winner = False
    if auction.winner and request.user.is_authenticated:
        is_current_user_winner = (auction.winner.id == request.user.id)
    remaining_seconds = max(0, int((auction.end_time - timezone.now()).total_seconds()))
    data = {
        'current_price': str(auction.current_price),
        'status': auction.status,
        'winner': winner_censored,
        'is_winner': is_current_user_winner,
        'remaining_seconds': remaining_seconds,
    }
    return JsonResponse(data)