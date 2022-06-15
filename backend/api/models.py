from django.contrib.auth import get_user_model
from django.db import models


class Games(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.slug


class Stores(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class GameDetails(models.Model):
    game = models.ForeignKey(
        Games, on_delete=models.CASCADE)
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField()
    game_url = models.URLField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = ['game', 'store']

    def __str__(self) -> str:
        return f'{self.game}, {self.store}'


class Videos(models.Model):
    game_details = models.ForeignKey(GameDetails, on_delete=models.CASCADE)
    url = models.URLField()
    type = models.CharField(max_length=50)
    is_master = models.BooleanField()

    class Meta:
        unique_together = ['game_details', 'url']

    def __str__(self) -> str:
        return f'{self.game_details}, {self.type}'


class Images(models.Model):
    game_details = models.ForeignKey(GameDetails, on_delete=models.CASCADE)
    url = models.URLField()
    is_master = models.BooleanField()

    class Meta:
        unique_together = ['game_details', 'url']

    def __str__(self) -> str:
        return f'{self.game_details}'


class Platforms(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class AvailablePlatforms(models.Model):
    game_details = models.ForeignKey(GameDetails, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platforms, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['game_details', 'platform']

    def __str__(self) -> str:
        return f'{self.platform}, {self.game_details}'


class Reviews(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['game', 'user']

    def __str__(self) -> str:
        return f'{self.rating}, {self.game}, {self.user}'


class Visits(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['game', 'ip', 'created_at']

    def __str__(self) -> str:
        return f'{self.game}, {self.user}'


class Searches(models.Model):
    value = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.value}, {self.created_at}'
