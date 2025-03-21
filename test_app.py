import pytest
from models import models
from app import app, db


@pytest.fixture
def client():
  with app.app_context():  # Ensure database calls are within app context
        initDB()
        db.create_all()  # Ensure tables are created before tests
        yield app.test_client()
        truncateDB()

def initDB():
    DATABASE = 'test_emp_db.db'
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE)

    with app.app_context():
        db.create_all()  # Create tables if they don’t exist


def truncateDB():
    with app.app_context():
        models.Employee.query.delete()
        db.session.commit()



def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200


def test_index_response(client):
    response = client.get('/')
    assert b"Employee Data" in response.data
    assert models.Employee.query.count() == 0


def test_add(client):
    test_data = {'name': 'Mickey Test',
                 'gender': 'male',
                 'address': 'IN',
                 'phone': '0123456789',
                 'salary': '2000',
                 'department': 'Sales'}
    client.post('/add', data=test_data)
    assert models.Employee.query.count() == 1


def test_edit():
    client = app.test_client()
    response = client.post('/edit/0')
    assert response.status_code == 200
    assert b"Sorry, the employee does not exist." in response.data


def test_delete(client):
    test_data = {'emp_id': 0}
    response = client.post('/delete', data=test_data)
    assert response.status_code == 200
    assert b"Sorry, the employee does not exist." in response.data
