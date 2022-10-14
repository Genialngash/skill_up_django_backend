import pytest
from django.contrib.auth import get_user_model
from users.models import JobseekerProfile

User = get_user_model()

# def test_example():
#     assert 1 == 1

# # pytest -m "slow"
# @pytest.mark.slow
# def test_example_2():
#     assert 2 == 2


# @pytest.fixture(scope='session')
# def fixture1(): 
#     """Runs once per test function"""
#     print('run fixture 1')
#     return 1

# def test_fixture_2(fixture1):
#     num = fixture1
#     assert num == 1

# @pytest.fixture
# def yield_fixture():
#     print('Start test phase')
#     yield 6
#     print('End test phase')


# def test_fixture_3(yield_fixture):
#     assert yield_fixture == 6


# @pytest.mark.django_db
# def test_user_create():
#     User.objects.create_user(
#         'user@example.com',
#     )

#     assert User.objects.count() == 1


# @pytest.mark.django_db
# def test_db_does_not_persist():
#     count = User.objects.all().count()
#     assert count == 0


# @pytest.fixture()
# def user_1(db):
#     return User.objects.create_user('user@example.com',)

# @pytest.mark.django_db
# def test_set_check_pass(user_1):
#     user_1.set_password('new_password')
#     assert user_1.check_password('new_password') is True

# def test_check_email(user_2):
#     assert user_2.email == 'user@example.com'


# def test_create_new_user(new_staff_user):
#     print('nnewwww')
#     print(new_staff_user.email)
#     print(new_staff_user.first_name)
#     print(new_staff_user.last_name)
#     print(new_staff_user.is_staff)
#     print(new_staff_user.u_type)


#     # assert new_user.first_name == 'Mike'


# def test_create_staffuser(new_staff_user_2):
#     print(new_staff_user_2.is_staff)
#     print(new_staff_user_2.first_name)
#     print(new_staff_user_2.email)


# @pytest.mark.django_db
# def test_new_user(user_one):
#     count = User.objects.all().count()
#     print(user_one.email)

#     assert count == 1


