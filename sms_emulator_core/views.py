import json
import logging

import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from sms_emulator_core.models import SMSMessage, Enterprise
from sms_emulator_core.forms import SMSReceiveForm, SMSSendForm

logger = logging.getLogger(__name__)


class MainSearchView(View):
    http_method_names = ['get', 'post', 'delete']

    @staticmethod
    def get(request):
        return render(request, 'chat/chat.html', {
            'enterprises': Enterprise.objects.all()
        })

    @staticmethod
    def post(request):
        enterprise = request.POST.get('enterprise')
        phone_number = (
            request.POST.get('phone_number').replace(' ', '')
            if request.POST.get('phone_number') else None
        )

        sms_messages = SMSMessage.objects.filter(
            Q(from_sender=phone_number) | Q(to_receiver=phone_number),
            enterprise__name=enterprise,
        ).order_by('-creation')

        return render(request, 'chat/chat_messaging.html', {
            'sms_messages': sms_messages
        })

    @staticmethod
    def delete(request):
        deleting_params = SMSSendForm(request.GET)
        if deleting_params.is_valid():
            phone_number = deleting_params.cleaned_data['phone_number']
            enterprise = deleting_params.cleaned_data['enterprise']
            SMSMessage.objects.filter(
                Q(from_sender=phone_number) | Q(to_receiver=phone_number),
                enterprise__name=enterprise,
            ).delete()

            return JsonResponse({'status': 'Ok'}, status=200)
        else:
            return JsonResponse(
                {'form_errors': deleting_params.errors}, status=400
            )


class SMSSendView(View):
    """
    Send SMS to Gateway
    """
    @staticmethod
    def post(request):
        send_form = SMSSendForm(request.POST)
        if send_form.is_valid():
            enterprise = Enterprise.objects.get(
                name=send_form.cleaned_data['enterprise']
            )
            SMSMessage.objects.create(
                from_sender=send_form.cleaned_data['phone_number'],
                to_receiver='sms_emulator',
                text=send_form.cleaned_data['sms_message'],
                direction=SMSMessage.OUTGOING,
                enterprise=enterprise
            )

            r = requests.post(
                url=enterprise.webhook_url,
                data={
                    'from': send_form.cleaned_data['phone_number'],
                    'to': 'sms_emulator',
                    'text': send_form.cleaned_data['sms_message']
                }
            )

            logger.info(f"{r.status_code}: {r.text}")

            return JsonResponse({'status': 'Ok'}, status=200)
        else:
            return JsonResponse(
                {'form_errors': send_form.errors}, status=400
            )


class SMSReceiveView(View):
    """
    Receiving SMS from Gateway
    """
    @staticmethod
    def post(request):
        receive_form = SMSReceiveForm(json.loads(request.body))
        if receive_form.is_valid():
            enterprise = Enterprise.objects.get(
                name=receive_form.cleaned_data['enterprise']
            )
            SMSMessage.objects.create(
                from_sender=receive_form.cleaned_data['from'],
                to_receiver=receive_form.cleaned_data['to'],
                text=receive_form.cleaned_data['text'],
                direction=SMSMessage.INCOMING,
                enterprise=enterprise
            )

            return JsonResponse(
                {'status': 'Ok'}, status=200
            )
        else:
            return JsonResponse(
                {'form_errors': receive_form.errors}, status=400
            )
