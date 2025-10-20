from rest_framework import serializers
from .models import *
from users.validators import *
from .mixins import NestedCreateMixin, NestedUpdateMixin
from datetime import date
from users.reset_password import create_password


class UserSerializer(serializers.ModelSerializer):
    profile_type = serializers.PrimaryKeyRelatedField(queryset=ProfileType.objects.all(), many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined', 'profile_type', 'photo']
        read_only_fields = ['id', 'date_joined']

        
    def validate_first_name(self, name):
        if name and not validate_first_name(name):
            raise serializers.ValidationError({'first_name':'First name must be all alphabetic'})
        return name
        
    def validate_last_name(self, name):
        if name and not validate_last_name(name):
            raise serializers.ValidationError({'last_name':'Last name must be all alphabetic'})
        return name
    
    def validate_password(self, value):
            validate_password(value)  
            return value
    

class ProfileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileType
        fields = ['profile_type']  


class CreateUserSerializer(NestedCreateMixin, NestedUpdateMixin, serializers.ModelSerializer):
    profile_type = serializers.PrimaryKeyRelatedField(queryset=ProfileType.objects.all(), many=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_type', 'photo'] 
        extra_kwargs = {'password': {'write_only': True}}  
        read_only_fields = ['id']


    def create(self, validated_data):
        if 'password' not in validated_data:
            validated_data['password'] = create_password()

        profile_types = validated_data.pop('profile_type', None)
        password = validated_data.pop('password') 
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)  
        user.save()  
        user.profile_type.set(profile_types)  

        if profile_types:
            user.profile_type.set(profile_types)
        
        return user

    
    def validate_first_name(self, name):
        if name and not validate_first_name(name):
            raise serializers.ValidationError({'first_name':'First name must be all alphabetic'})
        return name
        
    def validate_last_name(self, name):
        if name and not validate_last_name(name):
            raise serializers.ValidationError({'last_name':'Last name must be all alphabetic'}) 
        return name   

    def validate_password(self, value):
            validate_password(value)  
            return value
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField(validators=[validate_password])
    new_password2 = serializers.CharField()