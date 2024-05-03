from rest_framework import serializers
from .models import StudentImage,StaffImage

class StudentImageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = StudentImage
        fields = "__all__"

class StaffImageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = StaffImage
        fields = "__all__"




