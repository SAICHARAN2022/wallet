from django.db import models
from django.contrib.auth.models import User

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_enabled = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"

    class Meta:
        db_table = 'custom_user_wallet'

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.transaction_type} - ${self.amount}"

    class Meta:
        db_table = 'custom_transaction'