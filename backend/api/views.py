import asyncio
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Games, Searches
from api.serializers import GameDetailsAPISerializer, GamesListAPISerializer
from api.utils.data_processing import fetch_data_from_stores

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class GameListAPIView(APIView):
    def get(self, request) -> Response:
        q = request.GET.get('q', '')
        if len(q.strip()) < 3:
            return Response({'error': 'Search query is too short'}, status=status.HTTP_400_BAD_REQUEST)

        # compatible_serches = [q]
        # compatible_serches.extend(q[:-i] for i in range(1, len(q) // 2))

        # searches = Searches.objects.filter(
        #     value__in=compatible_serches, updated_at__time__gt=timezone.now() - timedelta(hours=1))

        # if not searches:
        fetch_data_from_stores(q)
        # s, c = Searches.objects.get_or_create(value=q)
        # if not c:
        #     s.save()

        games = Games.objects.filter(
            Q(title__contains=q) | Q(slug__contains=q)
        ).prefetch_related(
            'gamedetails_set',
            'gamedetails_set__store',
            'gamedetails_set__videos_set',
            'gamedetails_set__images_set',
            'gamedetails_set__availableplatforms_set__platform'
        )

        serializer = GamesListAPISerializer(games, many=True)

        if data := serializer.data:
            return Response(data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': '*'})
        return Response([], status=status.HTTP_204_NO_CONTENT, headers={'Access-Control-Allow-Origin': '*'})


class GameDetailsAPIView(APIView):
    def get(self, request, slug: str) -> Response:
        if game := Games.objects.filter(slug=slug).first():
            serializer = GameDetailsAPISerializer(game)

            return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})
        return Response({}, status=status.HTTP_404_NOT_FOUND, headers={'Access-Control-Allow-Origin': '*'})
