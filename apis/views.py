from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Category, Variation, Product, Color
from .serializes import CategorySerializer, ProductSerializer, VariationSerializer, ColorSerializer, RegistrationSerializer
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from accounts.models import Account
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def category_api(request, slug=None):
    if request.method == 'GET':
        if slug:
            qs = get_object_or_404(Category, slug=slug)
            serializer = CategorySerializer(qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            qs = Category.objects.all()
            serializer = CategorySerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message':'object created successfully.'},
                status=status.HTTP_201_CREATED
            )
    elif request.method in ['PUT', 'PATCH']:
        category = get_object_or_404(Category, slug=slug)
        partial = request.method == 'PATCH'
        serializer = CategorySerializer(category, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Object updated successfully.'},
                status=status.HTTP_200_OK
            )
    elif request.method == 'DELETE':
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(
                {'message': 'Object deleted successfully.'},
                status=status.HTTP_204_NO_CONTENT
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def product_api(request):
    if request.method == 'GET':
        qs = Product.objects.all()
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def variation_api(request):
    if request.method == 'GET':
        qs = Variation.objects.filter(status=Variation.Status.AVAILABLE)
        serializer = VariationSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def color_api(request, slug=None):
    if request.method == 'GET':
        if slug:
            qs = get_object_or_404(Color, slug=slug)
            serializer = ColorSerializer(qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            qs = Color.objects.all()
            serializer = ColorSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ColorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message':'object created successfully.'},
                status=status.HTTP_201_CREATED
            )
    elif request.method in ['PUT', 'PATCH']:
        color      = get_object_or_404(Color, slug=slug)
        partial    = request.method == 'PATCH'
        serializer = ColorSerializer(color, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Object updated successfully.'},
                status=status.HTTP_200_OK
            )
    elif request.method == 'DELETE':
        color = get_object_or_404(Color, slug=slug)
        color.delete() 
        return Response(
                {'message': 'Object deleted successfully.'},
                status=status.HTTP_204_NO_CONTENT
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Registrationuser_api(request):
    data       = request.data
    serializer = RegistrationSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.save()

        #send_verification_email
        uidb64          = urlsafe_base64_encode(force_bytes(user.pk))
        token           = default_token_generator.make_token(user)
        activation_link = f'http://127.0.0.1:8000/v1/api/activate/{uidb64}/{token}'
        email           = user.email
        send_email      = EmailMessage(
            subject     = 'Activation Email',
            body        = f'please click the link to active your account:{activation_link}',
            from_email  = settings.DEFAULT_FROM_EMAIL,
            to          = [email],
        )
        send_email.send()
        return Response({
            'message':'Account created, Check your email to activate ur account.'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def Activate_api(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response( {'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
        return Response( {"message":"Your activation link is invalid."}, status=status.HTTP_400_BAD_REQUEST)
    
    except Account.DoesNotExist:
        return Response({'message':"User Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'message': str(e)}, 500)


@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'message':'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {'message':'successfully logged out.'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error':'invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )





















































