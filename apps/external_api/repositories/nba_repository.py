from apps.api.models import NBAResult


class NBARepository:

    def __init__(self):
        pass

    def get_results_by_game_id(self, game_id):
        try:
            game = NBAResult.objects.get(game_id=game_id)
        except Exception as e:
            return None
        return game