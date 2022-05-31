"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from raterapi.models.game import Game
from raterapi.models.gamer import Gamer


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """The retrieve method will get a single object 
        from the database based on the pk (primary key) in 
        the url. We will use the ORM to get the data, then the 
        serializer to convert the data to json. Add the 
        following code to the retrievemethod, making sure 
        the code is tabbed correctly:

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """The list method is responsible for getting 
        the whole collection of objects from the database. 
        The ORM method for this one is all. Here is the code 
        to add to the method:

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        # Add in the next 3 lines
        gamer = request.query_params.get('id', None)
        if gamer is not None:
            games = games.filter(gamer_id=gamer)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a game
        # game = Game.objects.get(pk=pk)
        # game.title = request.data["title"]
        # game.maker = request.data["maker"]
        # game.number_of_players = request.data["number_of_players"]
        # game.skill_level = request.data["skill_level"]

        # game_type = GameType.objects.get(pk=request.data["game_type"])
        # game.game_type = game_type
        # game.save()

        # return Response(None, status=status.HTTP_204_NO_CONTENT)

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        game.categories.remove(*game.categories.all())
        game.categories.add(*request.data['categories'])

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        """Handle POST operations
        OLD CODE WITHOUT VALIDATION CHECK:
        def create(self, request):

        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            gamer=gamer,
            game_type=game_type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)

        Returns:
            Response -- JSON serialized game instance
        """
        # Any foreign keys needed must be stored in a variable
        # like this

        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        game = Game.objects.get(pk=serializer.data['id'])
        game.categories.add(*request.data['categories'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    The serializer class determines how the Python data should
    be serialized to be sent back to the client. Put the
    following code at the bottom of the same module as above.
    Make sure it is outside of the view class.
    """
    class Meta:
        model = Game
        fields = (
            'id',
            'title',
            'description',
            'designer',
            'year_released',
            'number_of_players',
            'play_time',
            'age_req',
            'gamer',
            'categories'
        )
        # depth = 2


class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id',
            'title',
            'description',
            'designer',
            'year_released',
            'number_of_players',
            'play_time',
            'age_req'
        )
        # depth = 2
