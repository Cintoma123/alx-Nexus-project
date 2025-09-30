from django.shortcuts import render
# Create your views here.

import requests, json, hmac, hashlib
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from payments_paystack.models import Payment
from payments_paystack.serializers import PaymentSerializer


class InitializePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = request.data.get("amount")

        # 1. Create order
        order = Order.objects.create(user=user, amount=amount)
        # 2. Initialize with Paystack
        url = "https://api.paystack.co/transaction/initialize"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        data = {
            "email": user.email,
            "amount": int(float(amount) * 100),  # Paystack expects kobo
            "callback_url": "https://your-frontend.com/payment/callback/",
        }
        r = requests.post(url, headers=headers, json=data).json()

        if r.get("status"):
            auth_url = r["data"]["authorization_url"]
            reference = r["data"]["reference"]

            Payment.objects.create(order=order, reference=reference, amount=amount)

            return Response({"authorization_url": auth_url, "reference": reference})
        return Response({"error": "Failed to initialize payment"}, status=400)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reference):
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.get(url, headers=headers).json()

        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if r.get("status") and r["data"]["status"] == "success":
            payment.status = "success"
            payment.channel = r["data"]["channel"]
            payment.save()

            order = payment.order
            order.status = "paid"
            order.save()

            return Response({"message": "Payment successful", "order_id": order.id})
        else:
            payment.status = "failed"
            payment.save()
            return Response({"message": "Payment failed"}, status=400)


@csrf_exempt
def paystack_webhook(request):
    signature = request.headers.get("X-Paystack-Signature")
    body = request.body
    expected_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode("utf-8"),
        body,
        hashlib.sha512
    ).hexdigest()

    if signature != expected_signature:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    event = json.loads(body)

    if event["event"] == "charge.success":
        reference = event["data"]["reference"]
        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = "success"
            payment.channel = event["data"]["channel"]
            payment.save()

            order = payment.order
            order.status = "paid"
            order.save()
        except Payment.DoesNotExist:
            pass

    return JsonResponse({"status": "ok"})

