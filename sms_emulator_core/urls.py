from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from sms_emulator_core import views

urlpatterns = [
    path(
        '', views.MainSearchView.as_view(),
        name='main'
    ),
    path(
        'outbox_message', views.SMSSendView.as_view(),
        name='outbox_message'
    ),
    path(
        'inbox_message', csrf_exempt(views.SMSReceiveView.as_view()),
        name='inbox_message'
    )
]
