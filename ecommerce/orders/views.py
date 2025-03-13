from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from authentication.models import User
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s')

class OrderListCreateView(APIView):
    '''Have GET and POST methods -
    GET method is to list order
    POST method only for customer, who can only place the order '''

    def get(self, request):
        '''GET method for list the order'''
        logging.info(
                f'user: {request.user}, user_type: {request.user.user_type}')
        if request.user.user_type == 'admin':
            orders = Order.objects.all()
        elif request.user.user_type == 'delivery_agent':
            orders = Order.objects.filter(delivery_agent=request.user)
        else:
            orders = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        ''' Only customers can place orders.'''
        logging.info(
                f'user: {request.user}, user_type: {request.user.user_type}')
        if request.user.user_type != 'customer':
            return Response({'error': 'Only customers can place orders'}, status=403)
        serializer = OrderSerializer(
                data={**request.data, 'customer': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class OrderAssignView(APIView):
    '''POST request for assign delivery_agent'''

    def post(self, request, order_id):
        logging.info(
                f'user: {request.user}, user_type: {request.user.user_type}')
        logging.info(f'Order id: {order_id}')
        agent_id = request.data['agent_id']
        logging.info(f'agent_id id: {agent_id}')
        if request.user.user_type != 'admin':
            return Response({'error': 'Permission denied'}, status=403)
        order = Order.objects.get(id=order_id)
        order.delivery_agent = User.objects.get(id=agent_id)
        order.status = 'ASSIGNED'
        order.save()
        return Response(OrderSerializer(order).data)

class OrderStatusUpdateView(APIView):
    '''PUT request for update the status'''
    def put(self, request, order_id):
        logging.info(
                f'user: {request.user}, user_type: {request.user.user_type}')
        if request.user.user_type != 'delivery_agent':            
            return Response({'error': 'Permission denied'}, status=403)
        order = Order.objects.get(id=order_id, delivery_agent=request.user)
        order.status = 'DELIVERED'
        order.save()
        return Response(OrderSerializer(order).data)

class OrderReportView(APIView):
    '''GET method is for list the order report'''
    def get(self, request):
        if request.user.user_type == 'admin':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)