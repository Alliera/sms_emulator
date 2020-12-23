import json

import requests
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from sms_emulator_core.models import Enterprise, SMSMessage


class SearchView(View):
    @staticmethod
    def get(request):
        return render(request, 'chat/chat.html')

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


class SMSSendView(View):
    """
    Send SMS to Gateway
    """
    @staticmethod
    def post(request):
        enterprise_name = request.POST.get('enterprise')
        from_sender = request.POST.get('phone_number')
        sms_message = request.POST.get('sms_message')

        if not all([enterprise_name, from_sender, sms_message]):
            return HttpResponse(
                'Not all fields has been received!', status=400
            )

        enterprise = Enterprise.objects.get(name=enterprise_name)

        SMSMessage.objects.create(
            from_sender=from_sender.replace(' ', ''),
            to_receiver='sms_emulator',
            text=sms_message,
            direction=SMSMessage.OUTGOING,
            enterprise=enterprise
        )

        r = requests.post(url=enterprise.webhook_url, data={
            'from': from_sender.replace(' ', ''),
            'to': 'sms_emulator',
            'text': sms_message
        })

        print(r.text)

        return JsonResponse({'status': 'Ok'}, status=200)


class SMSReceiveView(View):
    """
    Receiving SMS from Gateway
    """
    @staticmethod
    def post(request):
        data = json.loads(request.body)
        enterprise_name = data.get('enterprise')
        from_sender = data.get('from')
        to_receiver = data.get('to')
        sms_message = data.get('text')

        if not all([enterprise_name, from_sender, sms_message]):
            return HttpResponse(
                'Not all fields has been received!', status=400
            )

        enterprise = Enterprise.objects.get(name=enterprise_name)

        SMSMessage.objects.create(
            from_sender=from_sender.replace(' ', ''),
            to_receiver=to_receiver,
            text=sms_message,
            direction=SMSMessage.INCOMING,
            enterprise=enterprise
        )

        return JsonResponse({'status': 'Ok'}, status=200)


class ChatView(View):
    @staticmethod
    def get(request):
        return render(request, 'chat/chat.html')
