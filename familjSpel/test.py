from django.test import TestCase
from .models import GameSession

class AnimalTestCase(TestCase):
    def setUp(self):
        GameSession.objects.create(code='Z1HJWW490000QQ', question="Banana", state=0, category="banana", voting_done=False)

    def testGameSessionSetup(self):
        lion = GameSession.objects.get(code="Z1HJWW490000QQ")
        self.assertEqual(lion.question, 'Banana')