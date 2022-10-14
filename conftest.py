import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register

from tests.factories import JobseekerFactory, UserFactory

# accessed as user_factory
register(UserFactory)
register(JobseekerFactory)

User = get_user_model()


# @pytest.fixture()
# def user_2(db):
#     user = User.objects.create_user('user@example.com')
#     return user


# @pytest.fixture()
# def new_user_factory(db):
#     def create_app_user(
#         email: str = 'user@testing.com',
#         first_name: str = 'John',
#         last_name: str = 'Doe',
#         password: str = None,
#         u_type: str = 'Jobseeker',
#         is_staff: bool = False,
#         is_superuser: bool = False,
#         is_active: bool = False,
#     ):
#         user = User.objects.create_user(
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             password=password,
#             u_type=u_type,
#             is_staff=is_staff,
#             is_superuser=is_superuser,
#             is_active=is_active
#         )
#         return user
#     return create_app_user


# @pytest.fixture
# def new_staff_user(db, new_user_factory):
#     user = new_user_factory(
#         'mike@email.com', 'Mike', 'Wilkins',
#         'testing321', 'Employer',
#     )

#     user.is_staff = True
#     user.save()

#     return user


# @pytest.fixture
# def new_staff_user_2(db, new_user_factory):
#     user = new_user_factory(
#         email='livey@email.com',
#     )

#     user.is_staff = True
#     user.save()
#     return user


@pytest.fixture
def jobjseeker_one(db, jobseeker_factory):
    jobseeker = jobseeker_factory.create()
    return jobseeker


@pytest.fixture
def user_one(db, user_factory):
    user = user_factory.create()
    return user
