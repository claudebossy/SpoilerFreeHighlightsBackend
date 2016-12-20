from django.http import JsonResponse

from apps.external_api.services.nba_service import nba_service_instance


def nba_results(request, year, month, day):
    results = nba_service_instance.get_day_results(year, month, day)

    return JsonResponse(results, safe=False)
