from django.urls import path
from .views import (
    IndexView,
    ClassListView,
    ClassDetailView,
    StudentDetailView,
    TakeAttendanceView,
    AttendanceReportListView,
    AttendanceReportDetailView,
)

app_name = 'attendance'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('classes/', ClassListView.as_view(), name='class_list'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class_detail'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('take_attendance/<int:pk>/', TakeAttendanceView.as_view(), name='take_attendance'),
    path('attendance_reports/', AttendanceReportListView.as_view(), name='attendance_report_list'),
    path('attendance_reports/<int:pk>/', AttendanceReportDetailView.as_view(), name='attendance_report_detail'),
]
