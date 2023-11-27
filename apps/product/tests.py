from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth import  get_user_model

from apps.account.views import LoginView
from apps.category.models import Category
from apps.product.models import Product
from apps.product.views import ProductViewSet

# Create your tests here.
User = get_user_model()
class ProductTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setup_user()
        self.access_token = self.setup_user_token()
        self.setup_category()
        self.setup_product()


    def setup_user(self):
        return User.objects.create_superuser("test@gmail.com", '1')

    def setup_product(self):
        products = [
            Product(owner=self.user, category=Category.objects.first(), price=20,
                    image='image', title='test'),
            Product(owner=self.user, category=Category.objects.first(), price=20,
                        image='image', title='test1'),
            Product(owner=self.user, category=Category.objects.first(), price=20,
                    image='image', title='test2')
        ]
        Product.objects.bulk_create(products)


    def setup_category(self):
        Category.objects.create(name='category1')

    def setup_user_token(self):
        data = {
            'email' : "test@gmail.com",
            'password': '1'
        }
        request = self.factory.post('api/v1/account/login', data)
        view = LoginView.as_view()
        response = view(request)
        print(response)
        return response.data['access']


    def test_get_product(self):
        request = self.factory.get('api/v1/product')
        view = ProductViewSet.as_view({'get': 'list'})
        response = view(request)
        print(response)
        assert response.status_code == 200
        assert Product.objects.count() == 3

    def test_post_product(self):
        image = open('/Users/atai/Documents/maker/django/shop_api/media/products/JPEG_example_down.jpg', 'rb')
        data = {
            'owner': self.user.id,
            'category': Category.objects.first().slug,
            'title': 'test_post',
            'price': 20,
            'image': image,
            'stock': 'in_stock'
        }
        request = self.factory.post('api/v1/rpoduct/', data, HTTP_AUTHORIZATION='Bearer '+ self.access_token)
        view = ProductViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == 201


