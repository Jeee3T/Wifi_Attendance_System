from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Class(models.Model):
    """Model representing a class."""
    name = models.CharField(max_length=200, help_text='Enter the name of the class')
    students = models.ManyToManyField('Student', related_name='classes')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this class."""
        return reverse('class_detail', args=[str(self.id)])

class Student(models.Model):
    """Model representing a student."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    _classes = models.ManyToManyField('Class', help_text='Select a class for this student', blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this student."""
        return reverse('student_detail', args=[str(self.id)])

class AttendanceForm(models.Model):
    """Model representing a student's attendance for a particular class on a particular day."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    taken_by = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, null=True, blank=True)
    present = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.student} - {self.class_name} - {self.date}'

class AttendanceReport(models.Model):
    """Model representing a report of student attendance for a particular class over a specified time period."""
    attendance_form = models.ForeignKey(AttendanceForm, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.class_name} - {self.start_date} to {self.end_date}'

    class Meta:
        unique_together = ('attendance_form', 'student', 'class_name', 'status', 'start_date', 'end_date')
