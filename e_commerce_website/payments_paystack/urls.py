from django.urls import path
from payments_paystack.views import InitializePaymentView, VerifyPaymentView, paystack_webhook

urlpatterns = [
    path("initialize/", InitializePaymentView.as_view(), name="initialize-payment"),
    path("verify/<str:reference>/", VerifyPaymentView.as_view(), name="verify-payment"),
    path("webhook/", paystack_webhook, name="paystack-webhook"),
]
