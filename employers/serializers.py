from rest_framework import serializers

from .models import JobOffer


class JobOfferCreateSerializer(serializers.ModelSerializer):
    """
    Create or make a job offer.
    """

    class Meta:
        model = JobOffer
        fields = ('job_card','job_application','applicant',)


class AcceptJobOfferSerializer(serializers.Serializer):
    """
    Accept a job offer.
    """

    is_accepted = serializers.BooleanField(required=True, allow_null=False)

    def update(self, instance, validated_data):
        instance.is_accepted = validated_data.get('is_accepted', instance.is_accepted)
        return instance


class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ('id', 'job_card','job_application','applicant',)
