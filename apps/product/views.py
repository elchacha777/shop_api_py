from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import  ModelViewSet
from rest_framework.decorators import action, api_view
from apps.product.models import Product
from apps.product.permissons import IsAuthor
from apps.product.serializers import ProductSerializer
import  logging

from apps.rating.serializers import RatingSerializer

logger = logging.getLogger(__name__)

class StandartPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandartPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title',)
    filterset_fields = ('category',)



    def perform_create(self, serializer):
        # logger.info(self.request.user)
        # logger.error('Error here')
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticatedOrReadOnly()]

    @action(["GET", 'POST', 'DELETE'], detail=True)
    def rating(self, request, pk):
        product = self.get_object()
        user = request.user
        # localhost:8000/v1/api/products/2/rating

        if request.method == 'GET':
            ratings = product.ratings.all()
            serializer = RatingSerializer(instance=ratings, many=True).data
            return Response(serializer, status=200)
        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                return Response('You already rated ths product', status=400)
            data = request.data
            serializer = RatingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return Response(serializer.data, status=201)
        else:
            if not product.ratings.filter(owner=user).exists():
                return Response('You didnt rated this product')
            rating = product.ratings.get(owner=user)
            rating.delete()
            return Response('Deleted', status=204)



@api_view(["GET"])
def get_hello(request):
    print(request.hello)
    return Response('Hello')




