from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, UserWallet, Transaction
from .serializer import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.contrib import messages

from django.shortcuts import render
from django.views.generic import View

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework import status

from django.http import JsonResponse

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve wallet and transaction information
        wallet_information = UserWallet.objects.filter(user=request.user).select_related('user').values('id', 'user__username', 'balance')

        transaction_information = Transaction.objects.filter(added_by=request.user).order_by('-timestamp').values()
        wallet_serializer = UserWalletSerializer(wallet_information, many=True)
        return Response({
            'wallet': wallet_serializer.data,
            'transactions': transaction_information
        })

class AddFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Deserialize the input
        serializer = FundsSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            
            # Get or create the user's wallet
            user_wallet, created = UserWallet.objects.get_or_create(user=request.user)
            
            # Update the balance
            user_wallet.balance += amount
            user_wallet.save()

            # Record the transaction
            Transaction.objects.create(
                amount=amount,
                transaction_type='DEPOSIT',
                added_by=request.user
            )

            return Response({"message": "Funds added successfully.", "new_balance": str(user_wallet.balance)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SubtractFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Deserialize the input
        serializer = FundsSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            
            # Get or create the user's wallet
            user_wallet = UserWallet.objects.filter(user=request.user).first()
            
            if not user_wallet.balance > amount:
                return Response({"message": "Insufficient funds.", "currrent_balance": str(user_wallet.balance)}, status=status.HTTP_200_OK)
            # Update the balance
            user_wallet.balance -= amount
            user_wallet.save()

            # Record the transaction
            Transaction.objects.create(
                amount=amount,
                transaction_type='WITHDRAW',
                added_by=request.user
            )

            return Response({"message": "Funds Withdrawed successfully.", "new_balance": str(user_wallet.balance)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class login_view(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        get_user_object = User.objects.filter(email=email).first()
        if not get_user_object:
            return Response({'error': 'User Does Not exist'}, status=status.HTTP_400_BAD_REQUEST)


        # Authenticate the user
        user = authenticate(username=get_user_object.username, password=password)
        if user is not None:
            # Prepare the data for the token request
            data = {
                'grant_type': 'password',  # Using password grant type
                'username': get_user_object.username,
                'password': password,
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.SECRET_KEY,
            }

            # Send the request to the o/token endpoint
            token_url = 'http://127.0.0.1:8000/o/token/'  # Replace with your domain
            response = requests.post(token_url, data=data)

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials or token error'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class enable_status(APIView):
    permission_classes  = [IsAuthenticated]

    def post(self, request):
        # Extract the user and the new status from the request
        user = request.user
        is_enabled = request.data.get('is_enabled')

        if is_enabled is None:
            return Response({'detail': 'The "is_enabled" field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the user's wallet
            wallet = UserWallet.objects.get(user=user)
        except UserWallet.DoesNotExist:
            return Response({'detail': 'Wallet not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the wallet's status
        wallet.is_enabled = is_enabled
        wallet.save()
        return Response({
            'detail': 'Wallet status updated successfully.',})



