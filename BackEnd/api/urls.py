from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'exercises', views.ExerciseViewSet, basename='exercises')
router.register(r'exercises-history',
                views.ExerciseHistoryViewSet, basename='exercisehistory')
router.register(r'routine', views.RoutineViewSet, basename='routine')
router.register(r'routine-exercises',
                views.RoutineExercisesViewSet, basename='routineexercise')
router.register(r'record-weight', views.RecordWeightViewSet,
                basename='recordweight')
router.register(r'categories', views.CategorieViewSet, basename='categories')


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('api/csrf/', views.csrf),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]