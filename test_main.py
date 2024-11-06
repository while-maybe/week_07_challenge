import pytest

from main import Expenses, ExpensesAPI


@pytest.fixture
def test_data():
    data = Expenses()
    data.expenses = [
        {   "id": 1,
            "description": "Lunch",
            "amount": 10.5,
            "date": "2023-11-01"
        },
        {   "id": 2,
            "description": "Dinner",
            "amount": 21,
            "date": "2023-11-03"
        },
    ]
    yield data  # 
    del data    # removes the object
    
@pytest.fixture
def test_more_data():
    data = Expenses()
    data.expenses = [
        {   "id": 1,
            "description": "Lunch",
            "amount": 10.5,
            "date": "2023-11-01"
        },
        {   "id": 2,
            "description": "Dinner",
            "amount": 21,
            "date": "2023-11-03"
        },
        {   "id": 3,
            "description": "Beer",
            "amount": 3,
            "date": "2024-11-03"
        },
    ]
    yield data  # 
    del data    # removes the object


from unittest.mock import patch, Mock

# TODO investigate fixture scope!!!

# TODO autouse in fixtures
@pytest.mark.usefixtures("test_data")
class TestExpenses():
    
    @patch("requests.get")
    def test_load_expenses_mocked(self, mock_get, test_data):
        
        mock_response = Mock()
        mock_response.json.return_value = [
            {   "id": 1,
                "description": "Lunch",
                "amount": 10.5,
                "date": "2023-11-01"
            },
            {   "id": 2,
                "description": "Dinner",
                "amount": 21,
                "date": "2023-11-03"
            },
        ]
        
        mock_get.return_value = mock_response
        
        service_api = ExpensesAPI()
        # calls requests.get
        my_expenses = Expenses(service_api.load_expenses())
        
        assert my_expenses.expenses == test_data.expenses


    # test post
    @patch("requests.post")
    def test_post_expense_mocked(self, mock_post, test_data, test_more_data):
        
        new_expense = {
            "description": "Beer",
            "amount": 3,
            "date": "2024-11-03"
        },
        
        mock_response = Mock()
        # mock post expected json return 
        mock_response.json.return_value = {
            "id": 3,
            "description": "Beer",
            "amount": 3,
            "date": "2024-11-03"
        },
        mock_post.return_value = mock_response
        
        # given app.py returns 201 if post succesful so we do this as well
        mock_post.return_value.status_code = 201
        
        service_api = ExpensesAPI()
        
        # calls requests.post
        response = service_api.add_expense(new_expense)
        
        # loads inistial mock data to my_expenses
        my_expenses = test_data
        # append the response to existing starting data - response is a tuple, we only need the first element as don't want to include the http status code
        my_expenses.expenses.append(response.json()[0])

        assert my_expenses.expenses == test_more_data.expenses
        # assert http response code is 201 as this is in api
        assert response.status_code == 201
        

   # test put
    @patch("requests.put")
    def test_put_expense_mocked(self, mock_put):
             
        # new data and the the id of the destination expense in the api
        new_expense = {
            "description": "Brownie",
            "amount": 4,
            "date": "2024-11-03"
        }
        id_to_replace = 1
        
        mock_response = Mock()
        # mock post expected json return 
        mock_response.return_value = {
            "id": 1,
            "description": "Brownie",
            "amount": 4,
            "date": "2024-11-03"
        },
        mock_put.return_value.json.return_value = mock_response.return_value
        
        service_api = ExpensesAPI()
        
        # calls requests.put
        response = service_api.edit_expense(id_to_replace, new_expense)

        # assert if response is the same as the mock value with the correct id
        assert response.json() == mock_response.return_value

        # TEST FOR INVALID ID
        # updating an ID that doesn't exist, should return a 404
        invalid_id = 5
        # ...and an error return value
        mock_response = {'error': 'Expense not found'}
        mock_put.return_value.json.return_value = mock_response
        # given app.py returns 404 if not found
        mock_put.return_value.status_code = 404
        
        # calls requests.put with invalid_id and an expense
        response = service_api.edit_expense(invalid_id, new_expense)
        
        assert response.json() == {'error': 'Expense not found'}
        # assert http response code is 404 if not found
        assert response.status_code == 404

        
    # test delete api method, if delete is successful returns 204
    @patch("requests.delete")
    def test_del_expense_mocked(self, mock_delete):
        
        id_to_delete = 1
        
        mock_response = Mock()
        # expected response
        mock_response.return_value = ""
        
        mock_delete.return_value = mock_response
        mock_delete.return_value.status_code = 204
        
        service_api = ExpensesAPI()
        # calls requests
        response = service_api.del_expense(id_to_delete)
        
        # assert if we have an empty response as well as a 204 http return code
        assert response.return_value == ""
        assert response.status_code == 204
