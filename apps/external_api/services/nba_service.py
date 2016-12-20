import nba_py
from lxml import etree
import requests
from datetime import datetime
from apps.external_api.repositories.nba_repository import NBARepository
from django.core import serializers
import json


class NBAService:
    video_quality = {
        "high": "1280x720_3500",
        "medium": "",
        "low": ""
    }
    nba_team_mapping = {
        "ORL": "magic", "UTA": "jazz", "WAS": "wizards", "MIA": "heat", "DET": "pistons", "MEM": "grizzlies",
        "MIN": "timberwolves", "DEN": "nuggets", "POR": "blazers", "PHI": "sixers", "GSW": "warriors", "SAS": "spurs",
        "CHA": "hornets", "CLE": "cavaliers", "TOR": "raptors", "ATL": "hawks", "HOU": "rockets", "IND": "pacers",
        "PHX": "suns", "NYK": "knicks", "BOS": "celtics", "LAL": "lakers", "SAC": "kings", "CHI": "bulls",
        "OKC": "thunder", "MIL": "bucks", "BKN": "nets", "LAC": "clippers", "NOP": "pelicans", "DAL": "mavericks"
    }

    def __init__(self, nba_repository):
        if not isinstance(nba_repository, NBARepository):
            raise AttributeError("nba_repository is null or not an instance of NBARepository")
        self.nba_repository = nba_repository

    def get_nba_result(self, game_id):
        return self.nba_repository.get_results_by_game_id(game_id)

    def from_linescore_to_game_result(self, linescore, date, quality):
        game_results = {}
        for score in linescore:
            game_id = score["GAME_ID"]
            if game_id in game_results:
                game_results[game_id]["home_team"] = score["TEAM_ABBREVIATION"]
                game_results[game_id]["home_points"] = None if not score["PTS"] else int(score["PTS"])
            else:
                game_results[game_id] = {
                    "date": datetime.strptime(date, '%Y/%m/%d').date(),
                    "game_id": game_id,
                    "away_team": score["TEAM_ABBREVIATION"],
                    "away_points": None if not score["PTS"] else int(score["PTS"]),
                    "highlights": self.__get_highlights(
                        date,
                        self.nba_team_mapping[score["TEAM_ABBREVIATION"]],
                        quality)
                }
        return game_results

    def get_day_results(self, year, month, day, quality="high"):
        results = []
        scoreboard = nba_py.Scoreboard(month=int(month), day=int(day), year=int(year))
        date = "%s/%s/%s" % (year, month, day)

        game_results = self.from_linescore_to_game_result(scoreboard.line_score(), date, quality)

        for game_id in game_results:
            game = self.nba_repository.get_results_by_game_id(game_id)
            if game:
                if game.is_incomplete():
                    updated_game = self.nba_repository.update(game.id, game_results[game_id])
                    results.append(updated_game.serialize())
                else:
                    results.append(game.serialize())
            else:
                new_game = self.nba_repository.create(game_results[game_id])
                results.append(new_game.serialize())
        return results

    def __get_highlights(self, date, team, quality):
        video_quality = self.video_quality[quality]
        response = requests.get("http://www.nba.com/partners/video/elcidfeeds/team_%s.xml" % team)
        if response.status_code != 200:
            return None
        tree = etree.fromstring(response.content)
        for video in tree.xpath("/videos/video"):
            if video.get("cmsIIIid") and "recap" in video.get("cmsIIIid") and date in video.get("cmsIIIid"):
                for cut in video.xpath("videoCuts/videoCut"):
                    if "turner_mp4_%s" % video_quality == cut.get("key"):
                        return cut.text
        return None


nba_service_instance = None
