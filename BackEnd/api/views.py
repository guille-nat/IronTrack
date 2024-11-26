from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import transaction
from .models import (
    Exercises, ExercisesHistory,
    RoutineExercises, RecordsWeights, Categories, Routines
)
from .serializers import (
    UserSerializer, ExerciseSerializer,
    ExercisesHistorySerializer, RoutinesSerializer,
    RoutineExercisesSerializer, RecordsWeightsSerializer,
    CategoriesSerializer
)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = User(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            user.set_password(serializer.validated_data['password'])
            user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercises.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]


class ExerciseHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = ExercisesHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExercisesHistory.objects.filter(user=self.request.user)


class RoutineViewSet(viewsets.ModelViewSet):
    serializer_class = RoutinesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Routines.objects.filter(user=self.request.user)


class RoutineExercisesViewSet(viewsets.ModelViewSet):
    queryset = RoutineExercises.objects.all()
    serializer_class = RoutineExercisesSerializer
    permission_classes = [IsAuthenticated]


class RecordWeightViewSet(viewsets.ModelViewSet):
    serializer_class = RecordsWeightsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecordsWeights.objects.filter(id_user=self.request.user.id)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]
