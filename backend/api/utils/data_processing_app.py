import datetime

# from dateutil.relativedelta import relativedelta
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Avg, F, Count
from django.utils import timezone


# def toggle_favorite(game, user):
#     try:
#         favorite = Favorites.objects.get(game=game, user=user)
#         favorite.is_favorite = not favorite.is_favorite
#         favorite.save()
#     except Favorites.DoesNotExist:
#         favorite = Favorites.objects.create(game=game, user=user, is_favorite=True)
#         favorite.save()
#     return favorite


# def is_users_favorite(game, user):
#     try:
#         return Favorites.objects.get(game=game, user=user).is_favorite
#     except (Favorites.DoesNotExist, Reviews.DoesNotExist, TypeError):
#         return False


# def update_review(game, user, vote):
#     try:
#         if not 1 <= int(vote) <= 10:
#             raise ValueError
#         current_review, created = Reviews.objects.get_or_create(game=game, user=user)
#         current_review.vote = vote
#         current_review.save()
#         return current_review
#     except (Reviews.DoesNotExist, ValueError):
#         return None


# def get_game_or_create(title, unified_title, thumbnail_url):
#     game = Games.objects.filter(unified_title=unified_title).first()
#     if not game:
#         game = Games.objects.create(title=title, unified_title=unified_title, thumbnail_url=thumbnail_url)
#         game.save()
#     if not game.thumbnail_url:
#         game.thumbnail_url = thumbnail_url
#         game.save()
#     return game


# def get_user_rating(game, user):
#     try:
#         return Reviews.objects.get(game=game, user=user).vote
#     except (Games.DoesNotExist, Reviews.DoesNotExist, TypeError):
#         return None


# def get_average_rating(game):
#     try:
#         game_reviews = Reviews.objects.filter(game=game)
#         return round(sum(review.vote for review in game_reviews) / len(game_reviews), 2), len(game_reviews)
#     except (Games.DoesNotExist, Reviews.DoesNotExist, ZeroDivisionError):
#         return 0, 0


# def get_entries_count(game, from_date='all'):
#     all_entries = Entries.objects.all()
#     filtered_entries = filter_by_time(all_entries, from_date)
#     return filtered_entries.filter(game=game).values('game').annotate(entries_count=Count('game'))


# def register_new_entry(game, request: WSGIRequest):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')
#     else:
#         ip = request.META.get('REMOTE_ADDR')

#     if request.user.is_authenticated:
#         user = request.user
#     else:
#         user = None

#     entry = Entries.objects.filter(game=game, user=user, ip_address=ip).last()

#     if entry:
#         if entry.created.date() < datetime.date.today():
#             entry = Entries.objects.create(game=game, user=user, ip_address=ip)
#             entry.save()
#     else:
#         entry = Entries.objects.create(game=game, user=user, ip_address=ip)
#         entry.save()
#     return entry


# def get_games_with_best_rating(from_date):
#     all_reviews = Reviews.objects.all()
#     filtered_reviews = filter_by_time(all_reviews, from_date)
#     return filtered_reviews.values(
#         title=F('game__title'), thumbnail_url=F('game__thumbnail_url')
#     ).annotate(reviews_count=Count('vote'), average_rating=Avg('vote'))


# def get_games_with_most_favorites(from_date):
#     all_favorites = Favorites.objects.filter(is_favorite=True)
#     filtered_favorites = filter_by_time(all_favorites, from_date)
#     return filtered_favorites.values(
#         title=F('game__title'), thumbnail_url=F('game__thumbnail_url')
#     ).annotate(favorites_count=Count('game'))


# def get_games_with_most_entries(from_date):
#     all_entries = Entries.objects.all()
#     filtered_entries = filter_by_time(all_entries, from_date)
#     return filtered_entries.values(
#         title=F('game__title'), thumbnail_url=F('game__thumbnail_url')
#     ).annotate(entries_count=Count('game'))


# def get_favorite_games_with_best_rating(from_date, user):
#     all_reviews = Reviews.objects.filter(game__favorites__user=user, game__favorites__is_favorite=True)
#     filtered_reviews = filter_by_time(all_reviews, from_date)
#     result = filtered_reviews.values('game', title=F('game__title'), thumbnail_url=F('game__thumbnail_url')).annotate(reviews_count=Count('vote'), average_rating=Avg('vote'))
#     for item in result:
#         if review := filtered_reviews.filter(user=user, game_id=item['game']).first():
#             item['user_rating'] = review.vote
#         else:
#             item['user_rating'] = 0
#     return result


# def filter_by_time(db_objects, from_date):
#     valid_time_values = ['1d', '1w', '1m', '3m', '6m', '1y', 'all']

#     if from_date not in valid_time_values or from_date == 'all':
#         return db_objects

#     if from_date == '1d':
#         date = timezone.now() - datetime.timedelta(days=1)
#     elif from_date == '1w':
#         date = timezone.now() - datetime.timedelta(weeks=1)
#     elif from_date == '1m':
#         date = timezone.now() - relativedelta(months=1)
#     elif from_date == '3m':
#         date = timezone.now() - relativedelta(months=3)
#     elif from_date == '6m':
#         date = timezone.now() - relativedelta(months=6)
#     else:
#         date = timezone.now() - relativedelta(years=1)

#     return db_objects.filter(created__gt=date)


# def get_top_results(result, top):
#     valid_top_values = ['10', '25', '50', '100', '250', '1000', 'all']
#     if top not in valid_top_values:
#         return result[:10]
#     if top == 'all':
#         return result
#     else:
#         return result[:int(top)]


# def sort_ranking_by_column(result, sort_by, reverse):
#     if sort_by == 'title':
#         return sorted(result, key=lambda x: x['title'], reverse=reverse)
#     elif sort_by == 'reviews_count':
#         return sorted(result, key=lambda x: x['reviews_count'], reverse=reverse)
#     elif sort_by == 'average_rating':
#         return sorted(result, key=lambda x: x['average_rating'], reverse=reverse)
#     elif sort_by == 'user_rating':
#         return sorted(result, key=lambda x: x['user_rating'], reverse=reverse)
#     elif sort_by == 'entries_count':
#         return sorted(result, key=lambda x: x['entries_count'], reverse=reverse)
#     elif sort_by == 'favorites_count':
#         return sorted(result, key=lambda x: x['favorites_count'], reverse=reverse)


# def get_searched_games_count(user):
#     return Entries.objects.filter(user=user).count()


# def get_rated_games_count(user):
#     return Reviews.objects.filter(user=user).count()


# def get_favorites_games_count(user):
#     return Favorites.objects.filter(user=user, is_favorite=True).count()


# def get_all_games():
#     return Games.objects.values_list('title', flat=True)
