from rest_framework import serializers

from .models import JobseekerRating


class JobseekerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobseekerRating
        fields = ('__all__')
