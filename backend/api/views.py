from django.http import JsonResponse


def healthcheck(request):
    """
    Vista para mostrar el estado correcto de la API
    """
    return JsonResponse({"health": "ok"}, status=200)
