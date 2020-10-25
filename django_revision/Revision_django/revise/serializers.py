from rest_framework import serializers
from .models import PersonDetails

class PersonSerialize(serializers.ModelSerializer):
    class Meta:
        model = PersonDetails
        fields = ['id','name','email','phone_no','gender','address']
