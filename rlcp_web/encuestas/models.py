# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class LimeSurvey583965(models.Model):
    token = models.CharField(max_length=36, db_collation='utf8mb4_bin', blank=True, null=True)
    submitdate = models.DateTimeField(blank=True, null=True)
    lastpage = models.IntegerField(blank=True, null=True)
    startlanguage = models.CharField(max_length=20)
    seed = models.CharField(max_length=31, blank=True, null=True)
    edad = models.TextField(blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True, null=True)
    provincia = models.CharField(max_length=20, blank=True, null=True)
    universidad = models.CharField(max_length=10, blank=True, null=True)
    tipo_de_curso = models.CharField(db_column='tipo de curso', max_length=20, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    carrera = models.CharField(max_length=50, blank=True, null=True)
    año_academicco = models.CharField(db_column='año academicco', max_length=5, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    becado = models.CharField(max_length=5, blank=True, null=True)
    trabajas = models.CharField(max_length=5, blank=True, null=True)
    relacion_de_trabajo = models.CharField(db_column='relacion de trabajo', max_length=15, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    number_583965x17x432 = models.CharField(db_column='583965X17X432', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x17x433sq001 = models.TextField(db_column='583965X17X433SQ001', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x17x433sq002 = models.TextField(db_column='583965X17X433SQ002', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq001 = models.CharField(db_column='583965X21X436SQ001', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq002 = models.CharField(db_column='583965X21X436SQ002', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq003 = models.CharField(db_column='583965X21X436SQ003', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq004 = models.CharField(db_column='583965X21X436SQ004', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq005 = models.CharField(db_column='583965X21X436SQ005', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq006 = models.CharField(db_column='583965X21X436SQ006', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq007 = models.CharField(db_column='583965X21X436SQ007', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq008 = models.CharField(db_column='583965X21X436SQ008', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq009 = models.CharField(db_column='583965X21X436SQ009', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq010 = models.CharField(db_column='583965X21X436SQ010', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq011 = models.CharField(db_column='583965X21X436SQ011', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq012 = models.CharField(db_column='583965X21X436SQ012', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq013 = models.CharField(db_column='583965X21X436SQ013', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq014 = models.CharField(db_column='583965X21X436SQ014', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq015 = models.CharField(db_column='583965X21X436SQ015', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq016 = models.CharField(db_column='583965X21X436SQ016', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq017 = models.CharField(db_column='583965X21X436SQ017', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq018 = models.CharField(db_column='583965X21X436SQ018', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq019 = models.CharField(db_column='583965X21X436SQ019', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq020 = models.CharField(db_column='583965X21X436SQ020', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq021 = models.CharField(db_column='583965X21X436SQ021', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq022 = models.CharField(db_column='583965X21X436SQ022', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq023 = models.CharField(db_column='583965X21X436SQ023', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq024 = models.CharField(db_column='583965X21X436SQ024', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq025 = models.CharField(db_column='583965X21X436SQ025', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq026 = models.CharField(db_column='583965X21X436SQ026', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq027 = models.CharField(db_column='583965X21X436SQ027', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq028 = models.CharField(db_column='583965X21X436SQ028', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq029 = models.CharField(db_column='583965X21X436SQ029', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq030 = models.CharField(db_column='583965X21X436SQ030', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq031 = models.CharField(db_column='583965X21X436SQ031', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x21x436sq032 = models.CharField(db_column='583965X21X436SQ032', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x20x430 = models.CharField(db_column='583965X20X430', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_583965x20x430comment = models.TextField(db_column='583965X20X430comment', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'lime_survey_583965'



class GrupoRLCP(models.Model):
    id = models.BigAutoField(primary_key=True)
    ids_respuestas = models.TextField()
    patron_promedio = models.TextField()
    cantidad_miembros = models.IntegerField()

    class Meta:
        managed = False  # ¡Muy importante! Porque esta tabla ya existe
        db_table = 'grupos_rlcp'


class ConceptosGruposRLCP(models.Model):
    grupo = models.ForeignKey(GrupoRLCP, on_delete=models.CASCADE)
    testor = models.TextField()
    concepto = models.TextField()
    concepto_general = models.TextField()
    recomendacion = models.TextField()

    class Meta:
        db_table = 'conceptos_grupos_rlcp'  # 🔥 esto le dice a Django que no cree otra tabla
