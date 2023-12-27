from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.utils.html import strip_tags
from rest_framework.authentication import SessionAuthentication
from orders.models import Order
from orders.serializers import OrderSerializer
from cart.models import Cart, CartItem
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from orders.models import Order, OrderItem
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from Users.backends import UserProfileAuthBackend

class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        
        cart = Cart.objects.filter(user=user).first()  # Fetch the user's cart
        
        # Check if the cart exists
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            
            # Create the order with user
            order_data = {'user': user.id}
            order_serializer = self.get_serializer(data=order_data)
            
            if order_serializer.is_valid():
                order = order_serializer.save()

                # Add associated products from cart items to the order
                for cart_item in cart_items:
                    product = cart_item.product  # Assuming 'product' is the related field in CartItem
                    item_price = product.price  # Fetch price from the related product
                    order_item = OrderItem.objects.create(order=order, product=product, quantity=cart_item.quantity, price=item_price)
                    order.items.add(product)  # Add the product to the order
                    
                    # Decrease product quantity upon placing the order
                    product.quantity -= cart_item.quantity
                    product.save()

                # Calculate total price and save the order
                order.update_total_price()
                order.save()

                # Sending email notification
                subject = 'Order Confirmation'
                from_email = 'nithin.raj101@outlook.com'
                to_email = [user.email]

                context = {'order': order}
                html_content = render_to_string('order_confirmation_email.html', context)

                msg = EmailMultiAlternatives(subject, '', from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                # Delete items from the cart after placing the order
                cart_items.delete()

                return Response(order_serializer.data)

        return Response({"message": "No items in the cart to place an order."}, status=400)


class OrderHistoryView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve orders for the authenticated user
        return Order.objects.filter(user=self.request.user)

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    #permission_classes = [IsAuthenticated]  # Only admins can view all orders

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    #permission_classes = [AdminPermission]  # Only admins can view order details

class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [UserProfileAuthBackend, SessionAuthentication]
    #permission_classes = [AdminPermission]  # Only admins can update order status
    
    def put(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status:
            old_status = order.status
            order.status = new_status
            order.save()

            # Send email notification if status changes
            if old_status != new_status:
                subject = f"Order Status Update: {new_status}"
                from_email = "nithin.raj101@outlook.com"  # Replace with your email
                to_email = order.user.email  # Assuming 'Order' model has a 'user' field

                # Render HTML template for email
                html_content = render_to_string('order_status_update_email.html', {
                    'new_status': new_status,
                    'order_id': order.id  # Pass other needed data to the template
                })

                text_content = strip_tags(html_content)  # Strip HTML tags for plain text email

                email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                email.attach_alternative(html_content, "text/html")
                email.send()

            return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'New status not provided'}, status=status.HTTP_400_BAD_REQUEST)