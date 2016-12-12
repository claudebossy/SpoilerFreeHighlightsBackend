from django.http import JsonResponse

from apps.api.models import NBAResult
from apps.external_api.services.nba_service import nba_service_instance


def nba_results(request, year, month, day):
    results = nba_service_instance.get_day_results(year, month, day)
    for index in results:
        if "skipSave" not in results[index]:
            result = NBAResult(**results[index])
            if result.id:
                result.save(force_update=True)
            else:
                result.save()

    return JsonResponse(results)
