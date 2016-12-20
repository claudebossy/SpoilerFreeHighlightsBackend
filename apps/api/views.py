from django.http import JsonResponse

from apps.api.models import NBAResult
from apps.external_api.repositories.nba_repository import NBARepository
from apps.external_api.services.nba_service import nba_service_instance
import json
from django.core import serializers


def nba_results(request, year, month, day):
    results = nba_service_instance.get_day_results(year, month, day)
    db_results = []
    for result in results:
        nba_result = None
        if "skipSave" not in result:
            nba_result = NBAResult(**result)
            if nba_result.id:
                nba_result.save(force_update=True)
            else:
                nba_result.save()
        else:
            nba_result = nba_service_instance.get_nba_result(result["game_id"])
        db_results.append(json.loads(serializers.serialize('json', [nba_result, ]))[0]["fields"])

    return JsonResponse(db_results, safe=False)
