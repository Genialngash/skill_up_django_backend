from rest_framework import status
from rest_framework.response import Response

from . import certifications, languages, work_experience


def handler(self, **kwargs):
    data = kwargs.get('data')
    profile = kwargs.get('profile')
    lang_serializer = kwargs.get('lang_serializer')
    cert_serializer = kwargs.get('cert_serializer')
    work_experience_serializer = kwargs.get('work_experience_serializer')
    action = kwargs.get('action')
    user = kwargs.get('user')

    lang_err = languages.handler(
        action=action,
        data=data, 
        lang_serializer=lang_serializer,
        profile=profile,
        user=user
    )

    if lang_err is not None:
        return Response(lang_err, status=status.HTTP_400_BAD_REQUEST)

    if lang_err is None:
        cert_err = certifications.handler(
            action=action,
            data=data,
            cert_serializer=cert_serializer,
            profile=profile
        )

        if cert_err is not None:
            return Response(cert_err, status=status.HTTP_400_BAD_REQUEST)

        if cert_err is None:
            work_exp_err = work_experience.handler(
                data=data, 
                work_experience_serializer=work_experience_serializer,
                profile=profile,
                action=action,
            )

            if work_exp_err is not None:
                return Response(work_exp_err, status=status.HTTP_400_BAD_REQUEST)

            if work_exp_err is None:
                return Response({
                    'status': 'ok',
                    'status_code': 200,
                    'message': 'Profile updated successfully.'
                }, status=status.HTTP_200_OK,)
