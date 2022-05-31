"""View module for handling requests about game types"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from raterapi.models.game import Game
from raterapi.models.gamer import Gamer
from raterapi.models.category import Category
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models.review import Review


class ReviewView(ViewSet):
    # """Level up game types view"""

    # def retrieve(self, request, pk):
    #     """The retrieve method will get a single object
    #     from the database based on the pk (primary key) in
    #     the url. We will use the ORM to get the data, then the
    #     serializer to convert the data to json. Add the
    #     following code to the retrievemethod, making sure
    #     the code is tabbed correctly:

    #     Returns:
    #         Response -- JSON serialized game type
    #     """
    #     try:
    #         game = Game.objects.get(pk=pk)
    #         serializer = ReviewSerializer(game)
    #         return Response(serializer.data)
    #     except Game.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # def list(self, request):
    #     """The list method is responsible for getting
    #     the whole collection of objects from the database.
    #     The ORM method for this one is all. Here is the code
    #     to add to the method:

    #     Returns:
    #         Response -- JSON serialized list of game types
    #     """
    #     games = Game.objects.all()
    #     # Add in the next 3 lines
    #     game_type = request.query_params.get('type', None)
    #     if game_type is not None:
    #         games = games.filter(game_type_id=game_type)

    #     serializer = ReviewSerializer(games, many=True)
    #     return Response(serializer.data)

    # def update(self, request, pk):
    #     """Handle PUT Requests"""
    #     game = Game.objects.get(pk=pk)
    #     serializer = CreateReviewSerializer(game, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        """summary"""
        # Any foreign keys needed must be stored in a variable
        # like this
        game = Game.objects.get(pk=request.query_params.get('game', None))
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    The serializer class determines how the Python data should
    be serialized to be sent back to the client. Put the
    following code at the bottom of the same module as above.
    Make sure it is outside of the view class.
    """
    class Meta:
        model = Review
        fields = (
            'id',
            'review',
            'game',
            'gamer'
        )
        depth = 2


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # uses an array because information is coming from
        # front-end
        fields = ('review',)
