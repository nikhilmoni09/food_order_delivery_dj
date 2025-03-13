from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Product
from .serializers import ProductSerializer
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s')

class ProductListCreateView(APIView):
    '''Both have GET and POST methods'''
    def get(self, request):
        ''' List all products'''
        category = request.query_params.get('category')
        logging.info(f'category: {category}')
        products = Product.objects.filter(category=category) if category else Product.objects.all()
        # many=True queryset contains mutiple items (a list of items) 
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        ''' The admin role only can create products/food'''
        logging.info(f'user_type: {request.user.user_type}, user: {request.user}')
        if not request.user.user_type == 'admin':
            return Response({'error': 'Permission denied'}, status=403)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request):
        product_id = request.data['product_id']
        logging.info(f'Product update attempt for ID {product_id} by {request.user.username}')
        if not request.user.user_type == 'admin':
            return Response({'error': 'Permission denied'}, status=403)
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logging.info(f'Product {product_id} updated successfully')
                return Response(serializer.data)
            logging.info(f'Product update failed: {serializer.errors}')
            return Response(serializer.errors, status=400)
        except Product.DoesNotExist:
            logging.error(f'Product {product_id} not found')
            return Response({'error': 'Product not found'}, status=404)
        
    def delete(self, request):
        product_id = request.data['product_id']
        logging.info(f'Product deletion attempt for ID {product_id} by {request.user.username}')
        if not request.user.user_type == 'admin':
            return Response({'error': 'Permission denied'}, status=403)
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            logging.info(f'Product {product_id} deleted successfully')
            return Response(status=204)
        except Product.DoesNotExist:
            logging.error(f'Product {product_id} not found')
            return Response({'error': 'Product not found'}, status=404)
