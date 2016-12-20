from django.http import JsonResponse

from apps.api.models import NBAResult
from apps.external_api.services.nba_service import nba_service_instance


def nba_results(request, year, month, day):
    results = nba_service_instance.get_day_results(year, month, day)
    for result in results:
        if "skipSave" not in result:
            nba_result = NBAResult(**result)
            if nba_result.id:
                nba_result.save(force_update=True)
            else:
                nba_result.save()

    return JsonResponse(results, safe=False)
