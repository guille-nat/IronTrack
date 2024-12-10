from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrAdmin
from django.contrib.auth.models import User, Group
from django.db import transaction
from .models import (
    Exercises, ExercisesHistory,
    RoutineExercises, RecordsWeights, Categories, Routines, UserProfile
)
from .serializers import (
    UserSerializer, ExerciseSerializer,
    ExercisesHistorySerializer, RoutinesSerializer,
    RoutineExercisesSerializer, RecordsWeightsSerializer,
    CategoriesSerializer
)
from guardian.shortcuts import assign_perm


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

    def get_permissions(self):
        """
        Define permisos específicos para cada acción
        """
        if self.action == 'create':  # Permite crear perfiles sin autenticación
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:  # PUT, PATCH, DELETE
            # Restringir a propietarios o administradores
            return [IsOwnerOrAdmin()]
        # Requiere autenticación para otras acciones
        return [IsAuthenticated()]

    def get_queryset(self):
        # Filtrar para devolver solo el usuario autenticado
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo usuario sin necesidad de autenticación.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Usar una transacción para garantizar que el usuario y el perfil se creen juntos
        with transaction.atomic():
            # Extraer los datos del perfil
            profile_data = serializer.validated_data.pop('userprofile', None)
            user = User(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', '')
            )
            user.set_password(serializer.validated_data['password'])
            user.save()

            # Crear el perfil asociado si se enviaron datos del perfil
            if profile_data:
                UserProfile.objects.update_or_create(
                    user=user, **profile_data)

            # Asignar el usuario al grupo "usuario" por defecto
            user_group, create = Group.objects.get_or_create(name='usuario')
            user.groups.add(user_group)

            # Asignar permisos específicos al usuario
            assign_perm('change_user', user, user)
            assign_perm('view_user', user, user)

        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)


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
    queryset = Routines.objects.all()
    serializer_class = RoutinesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        routine = serializer.save(id_user=self.request.user)

        # asignar permisos específicos al creador
        assign_perm('view_routine', self.request.user, routine)
        assign_perm('change_routine', self.request.user, routine)
        assign_perm('delete_routine', self.request.user, routine)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Routines.objects.all()
        return Routines.objects.filter(owner=self.request.user)


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
