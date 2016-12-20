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

    def update(self, id, game):
        updated_game = NBAResult(id=id, **game)
        updated_game.save()
        return updated_game

    def create(self, game):
        new_game = NBAResult(**game)
        new_game.save()
        return new_game