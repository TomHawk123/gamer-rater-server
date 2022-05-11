from tkinter import CASCADE
from django.db import models


class Rating(models.Model):
    rating = models.FloatField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
