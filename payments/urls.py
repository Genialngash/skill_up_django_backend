from django.urls import path

from payments import gen_views, session_view

urlpatterns = [
    path('config/', gen_views.StripeConfig.as_view(), name='stripe_config'),
    path('webhook/', session_view.StripeWebhook.as_view(), name='stripe_wh'),
    path('create-checkout-session/', session_view.StripeCheckoutView.as_view(), name='create_checkout_session'),
    # path('setup-intent/', session_view.SetupIntentView.as_view(), name='setup_intent'),
    # path('subscription/cancel/', session_view.CancelSubscription.as_view(), name='cancel_sub'),
    # path('create-payment-intent/', alt_views.StripeIntentView.as_view(), name='creat_payment_intent'),
    # path('pro-subscription-packages', session_view.SubPackagesListView.as_view(), name='pro_sub_plan'),
]
