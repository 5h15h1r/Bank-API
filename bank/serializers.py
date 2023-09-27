# serializers.py in the bank app
from rest_framework import serializers
from .models import Banks, Branch

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    bankName = serializers.CharField(source='bank.name', read_only=True)
    class Meta:
        model = Branch
        fields = ['ifsc', 'branch', 'address', 'city', 'district', 'state', 'bankName']
    
 
        
