from django.dispatch import receiver

from swe import signals as s


@receiver(s.member_created)
def receive_member_creation_signal(**kwargs):
    data = kwargs.get('data')
    if data:
        asset = data.get('asset')
        time = data.get('time')

