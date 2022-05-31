from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Gamer


class GamerView(ViewSet):

    def list(self, request):
        """The list method is responsible for getting 
        the whole collection of objects from the database. 
        The ORM method for this one is all. Here is the code 
        to add to the method:

        Returns:
            Response -- JSON serialized list of game types
        """
        gamers = Gamer.objects.all()
        serializer = GamerSerializer(gamers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """The retrieve method will get a single object
        from the database based on the pk (primary key) in
        the url. We will use the ORM to get the data, then the
        serializer to convert the data to json. Add the
        following code to the retrieve method, making sure
        the code is tabbed correctly:
        Returns:
            Response -- JSON serialized game type
        """
        try:
            gamer = Gamer.objects.get(pk=pk)
            serializer = GamerSerializer(gamer)
            return Response(serializer.data)
        except Gamer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests to get all game types
        Returns:
            Response -- 204
        """
        gamer = Gamer.objects.get(pk=pk)
        gamer.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Gamer
        fields = (
            'id',
            'user',
            'bio'
        )
        depth = 2
