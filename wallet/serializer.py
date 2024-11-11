from rest_framework import serializers
from .models import User,UserWallet

class ValidateUserSerializer(serializers.ModelSerializer):
    
    def validate(self,data):
        if not (data['username'] or data['password']):
            raise serializers.ValidationError("Please provide username and password")
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Creating a user with email as username
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class FundsSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

class UserWalletSerializer(serializers.ModelSerializer):
    # Assuming 'user' is a foreign key to the User model
    email = serializers.EmailField(source='user__username')

    class Meta:
        model = UserWallet
        fields = ['id', 'email', 'balance']
