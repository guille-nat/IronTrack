from rest_framework import viewsets
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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
from django.middleware.csrf import get_token


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

# Desactiva CSRF para pruebas (ver siguiente punto para protección adecuada)


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        response = JsonResponse({'detail': 'Success'})
        response.set_cookie(
            'access_token',
            str(refresh.access_token),
            httponly=True,
            secure=False,  # Para producción, esto debe ser True (HTTPS)
            samesite='Strict',
        )
        return response
    else:
        return JsonResponse({'detail': 'Invalid credentials'}, status=401)


@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    response = JsonResponse({'detail': 'Logged out'}, status=200)
    response.delete_cookie('access_token')  # Elimina la cookie JWT
    return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Valida datos del User
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Asegura que si algo falla no se cree el User
        with transaction.atomic():
            # Crear el usuario
            user = User(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            user.set_password(serializer.validated_data['password'])
            user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # Devolver solo usuario autenticado.
        user = self.request.user
        return User.objects.filter(id=user.id)


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercises.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]


class ExerciseHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = ExercisesHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra el queryset para devolver solo las entradas del usuario autenticado
        user = self.request.user
        return ExercisesHistory.objects.filter(user=user)


class RoutineViewSet(viewsets.ModelViewSet):
    serializer_class = RoutinesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra el queryset para devolver solo las entradas del usuario autenticado
        user = self.request.user
        return Routines.objects.filter(user=user)


class RoutineExercisesViewSet(viewsets.ModelViewSet):
    queryset = RoutineExercises.objects.all()
    serializer_class = RoutineExercisesSerializer
    permission_classes = [IsAuthenticated]


class RecordWeightViewSet(viewsets.ModelViewSet):
    serializer_class = RecordsWeightsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return RecordsWeights.objects.filter(id_user=user.id)


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]
