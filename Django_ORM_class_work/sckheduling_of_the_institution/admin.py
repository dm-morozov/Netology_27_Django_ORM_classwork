from django.contrib import admin
from .models import Schedule, Auditory, StudyGroup, Teacher

# Register your models here.


@admin.register(Schedule)
class SheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


@admin.register(Auditory)
class AuditoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'floor']
    inlines = [SheduleInline]


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    inlines = [SheduleInline]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']
    inlines = [SheduleInline]