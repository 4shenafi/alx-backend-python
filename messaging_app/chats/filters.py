import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by:
    - sender
    - conversation
    - time range (sent_at)
    """
    start_date = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["sender", "conversation", "start_date", "end_date"]
