from swe.models_serializer import SerializerMember


def create_member(data):
    user = SerializerMember(data=data)
    user.is_valid(raise_exception=True)
    user.save()