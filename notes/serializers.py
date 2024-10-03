from rest_framework import serializers

from notes.models import User,Task

class UserSerializer(serializers.ModelSerializer):


    password1=serializers.CharField(write_only=True) #p1 and p2 are not in model so we defined they here
    password2=serializers.CharField(write_only=True)

    password=serializers.CharField(read_only=True)

    class Meta:
        model=User

        fields=["id","username","email","password1","phone","password2","password"]

        
    def create(self,validate_data):

        password1=validate_data.pop("password1") #removing p1 and p2
        password2=validate_data.pop("password2")

        return User.objects.create_user(**validate_data,password=password1) #store p1 or p2 in password
    

    def validate(self,data):

        if data["password1"]!=data["password2"]:

            raise serializers.ValidationError("password mismatch")
        
        return data
    
class TaskSerializer(serializers.ModelSerializer):

    owner=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Task

        fields="__all__"

        read_only_fields=["id","created_date","owner","is_active"]



