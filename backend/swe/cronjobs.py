from django.utils import timezone

from swe.globals import STATUS_ACTIVE
from swe.models import Movie


def reset_daily_view():
    print("Time: " + str(timezone.now()) + " Reset Daily View")
    movies = Movie.objects.filter(status=STATUS_ACTIVE)
    movies.update(
        daily_view=0,
        last_update_date=timezone.now()
    )