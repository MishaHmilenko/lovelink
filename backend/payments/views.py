import stripe
from django.conf import settings
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.serializers import (CreateCheckOutSessionSerializer,
                                  ProductsSerializer)
from users.models import User


class StripeConfigAPIView(APIView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return Response(
            data={'publicKey': settings.STRIPE_PUBLISHABLE_KEY}, status=status.HTTP_200_OK)


class CreateCheckOutSession(CreateAPIView):
    serializer_class = CreateCheckOutSessionSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = self.get_stripe_product(serializer.validated_data['prod_id'])
        customer = self.get_or_create_stripe_customer(request.user)

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url='http://127.0.0.1:5500/success.html',
                cancel_url='http://127.0.0.1:5500/canceled.html',
                customer=customer,
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': product['default_price'],
                        'quantity': 1
                    }
                ]
            )
            return Response(data={'sessionId': checkout_session['id']}, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_stripe_product(self, prod_id):
        try:
            return stripe.Product.retrieve(prod_id)
        except stripe.error.InvalidRequestError as e:
            raise Http404({'error': str(e)})

    def get_or_create_stripe_customer(self, user):
        try:
            return stripe.Customer.list(email=user.email, limit=1).get('data')[0]
        except IndexError:
            return stripe.Customer.create(
                name=user.username,
                email=user.email,
            )


class GetAllProductsAPIView(ListAPIView):

    """ Getting all products from stripe.Product """

    serializer_class = ProductsSerializer

    def get_queryset(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return stripe.Product.list(active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class StripeWebHookAPIView(APIView):

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.headers.get('stripe-signature')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            print(f"Invalid payload: {e}")
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(f"Invalid signature: {e}")
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            customer = stripe.Customer.retrieve(event['data']['object']['customer'])
            user = User.objects.get(username=customer.name, email=customer.email)
            # Getting payment id
            payment_intent = stripe.PaymentIntent.retrieve(event['data']['object']['payment_intent'])
            # Adding coins to the user's account
            user.coins += payment_intent['amount'] / 100
            user.save()
            return Response(
                data={f'message': f'User\'s current account: {user.coins} love-coins'},
                status=status.HTTP_200_OK
            )
