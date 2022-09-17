from django.dispatch import receiver

from swe import signals as s
from swe import models as m


@receiver(s.member_created)
def receive_member_creation_signal(**kwargs):
    data = kwargs.get('data')
    if data:
        m.Log.objects.create(
            data=data
        )
