from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Exercises, ExercisesHistory,
    RoutineExercises, RecordsWeights, Categories, Routines
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email',
            'password', 'first_name', 'last_name'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


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
