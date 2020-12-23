from django.db import models


class Enterprise(models.Model):
    name = models.CharField(max_length=255)
    webhook_url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'enterprise'
        verbose_name = 'Enterprise'
        verbose_name_plural = 'Enterprises'


class SMSMessage(models.Model):

    INCOMING = 'Incoming'
    OUTGOING = 'Outgoing'

    from_sender = models.CharField(max_length=255)
    to_receiver = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    direction = models.CharField(
        choices=[(INCOMING, 'Incoming'), (OUTGOING, 'Outgoing')],
        max_length=255
    )
    creation = models.DateTimeField(auto_now_add=True)
    enterprise = models.ForeignKey(
        Enterprise, related_name='sms_messages', on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"From: {self.from_sender}, To: {self.to_receiver}, "
            f"Text: {self.text}"
        )

    class Meta:
        db_table = 'sms_message'
        verbose_name = 'SMS Message'
        verbose_name_plural = 'SMS Messages'
