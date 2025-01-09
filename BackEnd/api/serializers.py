from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Exercises, ExercisesHistory,
    RoutineExercises, RecordsWeights, Categories, Routines, UserProfile
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'birthday', 'created_at', 'nationality']
        read_only_fields = ('id', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Incluir el perfil de usuario
    profile = UserProfileSerializer(source='userprofile')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email',
            'password', 'first_name', 'last_name', 'profile'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        # Extraer los datos del perfil
        profile_data = validated_data.pop('userprofile', None)

        # Crear el usuario
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # Crear el perfil asociado si los datos del perfil están presentes
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        # Extraer datos del perfil
        profile_data = validated_data.pop('profile', None)

        # Actualizar datos del usuario
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Actualizar o crear el perfil
        if profile_data:
            UserProfile.objects.update_or_create(
                user=instance, defaults=profile_data)

        return instance


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = '__all__'
        read_only_fields = ('id',)


class ExercisesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercisesHistory
        fields = '__all__'
        read_only_fields = ('id',)


class RoutinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routines
        fields = '__all__'
        read_only_fields = ('id',)


class RoutineExercisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineExercises
        fields = '__all__'
        read_only_fields = ('id',)


class RecordsWeightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordsWeights
        fields = '__all__'
        read_only_fields = ('id',)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        read_only_fields = ('id',)
