import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Message
        fields = ['sender', 'sent_at']