from jobs.models import JobBookmark
from jobs.serializers import JobCardSlimSerializer
from rest_framework import serializers


class JobBookmarkRerieveSerializer(serializers.ModelSerializer):
    job_card = JobCardSlimSerializer()
    class Meta:
        model = JobBookmark
        fields = ('id', 'job_card',)
