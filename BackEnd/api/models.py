from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Categories(models.Model):
    """
    Modelo que representa las categorías de ejercicios.

    Attributes:
        name (str): Nombre de la categoría.
    """
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Exercises(models.Model):
    """
    Modelo que representa un ejercicio.

    Attributes:
        name (str): Nombre del ejercicio.
        type (str): Tipo de ejercicio (Máquina o Libre).
        img_exercise (ImageField): Imagen del ejercicio.
        description (str): Descripción del ejercicio.
        sets (int): Número recomendado de sets para el ejercicio.
        id_cat (ForeignKey): Relación con el modelo Categories.
    """
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[
        ('maquina', 'Máquina'), ('libre', 'Libre')])
    img_exercise = models.ImageField(upload_to='exercises/')
    description = models.TextField(max_length=600)
    sets = models.IntegerField(default=4)
    id_cat = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='exercises')

    def __str__(self) -> str:
        return self.name


class Routines(models.Model):
    """
    Modelo que representa una rutina de ejercicios para un usuario.

    Attributes:
        id_user (ForeignKey): Relación con el modelo User.
        day (str): Nombre del día en que se realiza la rutina (Lunes, Martes, etc.).
    """
    DAYS_OF_WEEK = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    id_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='routines')
    # Cambiado a CharField con opciones
    day = models.CharField(max_length=9, choices=DAYS_OF_WEEK, default='lunes')

    def __str__(self) -> str:
        # Muestra el nombre del día
        return f"{self.id_user.username} - {self.get_day_display()}"


class RoutineExercises(models.Model):
    """
    Modelo que representa la relación entre una rutina y sus ejercicios.

    Attributes:
        id_routine (ForeignKey): Relación con el modelo Routines.
        id_exercises (ForeignKey): Relación con el modelo Exercises.
    """
    id_routine = models.ForeignKey(
        Routines, on_delete=models.CASCADE, related_name='routine_exercises')
    id_exercises = models.ForeignKey(
        Exercises, on_delete=models.CASCADE, related_name='routine_exercises')

    def __str__(self) -> str:
        return f"{self.id_routine} - {self.id_exercises.name}"


class RecordsWeights(models.Model):
    """
    Modelo que representa el registro de pesos levantados por un usuario.

    Attributes:
        weights (float): Peso levantado en el ejercicio.
        date (date): Fecha en que se realizó el ejercicio.
        note (str): Notas adicionales sobre el entrenamiento.
        repetitions (int): Número de repeticiones realizadas.
        intensity (str): Intensidad del entrenamiento (baja, media, alta).
        id_user (ForeignKey): Relación con el modelo User.
        id_exercises (ForeignKey): Relación con el modelo Exercises.
    """
    # Asegura que el peso sea positivo
    weights = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateField()
    note = models.TextField(max_length=500)
    repetitions = models.IntegerField()
    # baja, media, alta, excelente entrenamiento
    intensity = models.CharField(max_length=50)
    id_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='records_weights')
    id_exercises = models.ForeignKey(
        Exercises, on_delete=models.CASCADE, related_name='records_weights')

    def __str__(self) -> str:
        return f"{self.id_exercises.name} - {self.date}"


class ExercisesHistory(models.Model):
    """
    Modelo que representa el historial de ejercicios realizados por un usuario.

    Attributes:
        id_user (ForeignKey): Relación con el modelo User.
        id_exercises (ForeignKey): Relación con el modelo Exercises.
        date (date): Fecha en que se realizó el ejercicio.
        weights (float): Peso levantado durante el ejercicio.
    """
    id_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='exercise_history')
    id_exercises = models.ForeignKey(
        Exercises, on_delete=models.CASCADE, related_name='exercise_history')
    date = models.DateField()
    # Asegura que el peso sea positivo
    weights = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"{self.id_exercises.name} - {self.date}"
