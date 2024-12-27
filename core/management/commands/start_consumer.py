from django.core.management.base import BaseCommand
from core.consumers import MultiBrokerConsumer
from django.conf import settings


class Command(BaseCommand):
    help = 'Démarre le consommateur Kombu'

    def handle(self, *args, **kwargs):
        consume = MultiBrokerConsumer(settings.KOMBU_BROKER_URLS)
        self.stdout.write("Démarrage du consommateur...")
        consume.consume()