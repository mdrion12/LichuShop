
from itertools import product
from tkinter.tix import Tree

from rest_framework.decorators import api_view,permission_classes
from .serializers import OrderCreationSerializer,orderserilizer,orderDetailSerializer
from .models import Customer,Order,Product,Order_item
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
@api_view(['POST'])
def order_create(request):
    serializer=OrderCreationSerializer(data=request.data)
    if serializer.is_valid():
        data=serializer.validated_data
        customer=data.get('Customer')
        product=data.get('product')
        customer_name=customer['name']
        customer_phone=customer['phone_number']
        customer_address=customer['address']
        customer,_=Customer.objects.get_or_create(name=customer_name,phone_number=customer_phone,address=customer_address)
        order=Order.objects.create(phone_number=customer,total_price=0)
        total_price=0
        for item in product:
            product_id=item.get('product_id')
            product_quantity=item.get('quantity')
            products=Product.objects.get(id=product_id)
            if products.stock < product_quantity:
                    return Response({"error": f"Not enough stock for {product.product_name}"}, status=status.HTTP_400_BAD_REQUEST)
            total_price+=products.price*product_quantity
            Order_item.objects.create(
                  order_id=order,
                  product_id= products,
                  quantity=product_quantity,
                  price=products.price*product_quantity
            )
            products.stock-=product_quantity
            products.save()
        order.total_price=total_price
        order.save()
        return Response({"message": "Order created successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orders(request):
     order=Order.objects.select_related('phone_number').filter(status='pending')
     serializer=orderserilizer(order,many=True)
     serializer.is_valid()
     return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orderstatus(request,order_status):
     order=Order.objects.select_related('phone_number').filter(status=order_status)
     serializer=orderserilizer(order,many=True)
     serializer.is_valid()
     return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def order_details(request, order_id):

    orderitem = Order_item.objects.select_related(
        'order_id__phone_number', 
        'product_id'
    ).filter(order_id=order_id)

    if not orderitem.exists():
        return Response({'error': 'Order not found'}, status=404)

    first_item = orderitem.first()
    customer_name = first_item.order_id.phone_number.name
    phone_number = first_item.order_id.phone_number.phone_number
    address = first_item.order_id.phone_number.address

    productlist = []
    for item in orderitem:
        products = {
            "product_name": item.product_id.product_name,
            "product_price": item.product_id.price,
            "product_description": item.product_id.product_description,
            "product_image": item.product_id.product_image.url if item.product_id.product_image else None,
            "product_quantity": item.quantity,
            "total_price": item.price
        }
        productlist.append(products)

    serializer = orderDetailSerializer(data={
        "customer_name": customer_name,
        "phone_number": phone_number,
        "address": address,
        "productlist": productlist
    })
    serializer.is_valid() 
    return Response(serializer.data, status=200)