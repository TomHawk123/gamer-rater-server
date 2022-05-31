from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    play_time = models.FloatField()
    age_req = models.IntegerField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        "Category",
        through="gameCategory",
        related_name="games"
    )

    @property
    def joined(self):
        """_summary_"""
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
