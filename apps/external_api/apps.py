from django.apps import AppConfig


class NBAConfig(AppConfig):
    name = 'apps.external_api'

    def ready(self):
        from apps.external_api.repositories.nba_repository import NBARepository
        from apps.external_api.services import nba_service
        nba_repository = NBARepository()
        nba_service.nba_service_instance = nba_service.NBAService(nba_repository)

