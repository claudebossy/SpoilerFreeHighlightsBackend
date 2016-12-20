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

    def get_day_results(self, year, month, day, quality="high"):
        results = []
        scoreboard = nba_py.Scoreboard(month=int(month), day=int(day), year=int(year))
        date = "%s/%s/%s" % (year, month, day)
        for score in scoreboard.line_score():
            game_id = score["GAME_ID"]
            game = self.nba_repository.get_results_by_game_id(game_id)
            if game and game.highlights is not None:
                db_entry = json.loads(serializers.serialize('json', [game, ]))[0]["fields"]
                db_entry["skipSave"] = True
                results.append(db_entry)
                continue
            api_result = {
                "name": score["TEAM_ABBREVIATION"],
                "points": score["PTS"]
            }
            result_list = [item for item in results if "game_id" in item and item["game_id"] == game_id]
            if len(result_list) > 0:
                result = result_list[0]
                result["home_team"] = api_result["name"]
                result["home_points"] = None if not api_result["points"] else int(api_result["points"])
            else:
                results.append({
                    "date": datetime.strptime(date, '%Y/%m/%d').date(),
                    "game_id": game_id,
                    "id": None if not game else game.id,
                    "away_team": api_result["name"],
                    "away_points": None if not api_result["points"] else int(api_result["points"]),
                    "highlights": self.__get_highlights(
                        date,
                        self.nba_team_mapping[api_result["name"]],
                        quality)
                })
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
