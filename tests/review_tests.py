from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapi.models import Gamer
from raterapi.models.review import Review
from raterapi.views.reviews import CreateReviewSerializer

class ReviewTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'categories', 'gameCategories', 'pictures', 'games', 'reviews']

    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_review(self):
        """Create review test"""
        url = "/reviews?game=1"

        # Define the Game properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        review = {
            "review": "Fantastico"
        }

        response = self.client.post(url, review, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # Get the last review added to the database, it should be the one just created
        new_review = Review.objects.last()

        expected = CreateReviewSerializer(new_review)

        # Now we can test that the expected output matches what was actually returned
        self.assertEqual(expected.data, response.data)