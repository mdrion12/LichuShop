
from rest_framework.decorators import api_view
from .serializers import OrderCreationSerializer
from .models import Customer,Order,Product,Order_item
from rest_framework.response import Response
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

        