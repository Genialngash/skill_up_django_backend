from django.urls import resolve, reverse


class TestEstablishmentUrls:
    def test_employee_list_view_exists(self):
        """
        Test that employee list url exists
        """
        path = reverse('employee_list_view')
        assert resolve(path).view_name == 'employee_list_view'


    def test_company_detail_view_exists(self):
        """
        Test that company view url exists
        """
        path = reverse('companies-detail', kwargs={'pk': 1})
        assert 'company' in resolve(path).route


    def test_company_list_create_view_exists(self):
        """
        Test that company create view url exists
        """
        path = reverse('companies-list')
        assert 'company' in resolve(path).route


    def test_user_companies_list_view_exists(self):
        """
        Test that user company list  view url exists
        """
        path = reverse('user-companies-list')
        assert 'my-companies' in resolve(path).route
