from django.http import HttpResponse
from datetime import date

class BlockWeekendOrdersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if date.today().weekday() >= 5 and request.path == '/api/orders/order_create/':
            return HttpResponse('Orders are not accepted on weekends.', status=403)
        response = self.get_response(request)
        return response