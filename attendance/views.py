from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views.generic.detail import DetailView
from .models import Class, Student, AttendanceForm, AttendanceReport
from .forms import AttendanceForm


class IndexView(generic.ListView):
    """View function for home page of site."""

    model = Class
    template_name = 'attendance/index.html'
    context_object_name = 'class_list'

class ClassListView(generic.ListView):
    """View to display a list of all classes."""

    model = Class
    template_name = 'attendance/class_list.html'
    context_object_name = 'class_list'

class ClassDetailView(generic.DetailView):
    """View to display details of a class."""

    model = Class
    template_name = 'attendance/class_detail.html'
    context_object_name = 'class_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_obj = self.get_object()
        students = class_obj.students.all()
        attendance_report_dates = AttendanceReport.objects.filter(class_name=class_obj).values_list(flat=True)
        context['students'] = students
        context['attendance_report_dates'] = attendance_report_dates
        return context


class StudentListView(generic.ListView):
    """View function for student list page."""

    model = Student
    template_name = 'attendance/student_list.html'
    context_object_name = 'student_list'

class StudentDetailView(generic.DetailView):
    """View to display details of a student."""

    model = Student
    template_name = 'attendance/student_detail.html'
    context_object_name = 'student_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_obj = self.get_object()
        attendance_reports = student_obj.attendance_reports.all()
        context['attendance_reports'] = attendance_reports
        return context

class TakeAttendanceView(generic.FormView):
    """View to take attendance for a class."""

    template_name = 'attendance/take_attendance.html'
    form_class = AttendanceForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        class_id = self.kwargs['class_id']
        class_obj = get_object_or_404(Class, id=class_id)
        kwargs['class_obj'] = class_obj
        return kwargs

    def form_valid(self, form):
        class_obj = form.cleaned_data['class_obj']
        date = form.cleaned_data['date']
        students = form.cleaned_data['students']
        attendance_records = []
        for student in students:
            attendance_records.append(
                AttendanceReport(
                    student=student,
                    date=date,
                    is_present=True
                )
            )
        AttendanceReport.objects.bulk_create(attendance_records)
        messages.success(self.request, 'Attendance taken successfully!')
        return redirect('class_detail', pk=class_obj.pk)


# @method_decorator(login_required, name='dispatch')
class AttendanceReportListView(generic.TemplateView):
    """View function for displaying attendance report."""

    model = AttendanceReport
    template_name = 'attendance/attendance_report_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.kwargs.get('class_id')
        student_id = self.kwargs.get('student_id')
        if class_id:
            queryset = queryset.filter(student__class_id=class_id)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        class_id = self.kwargs.get('class_id')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if class_id and start_date and end_date:
            attendance_report = AttendanceReport.objects.create(
                class_name=get_object_or_404(Class, pk=class_id),
                start_date=start_date,
                end_date=end_date
            )

            attendance_form_list = AttendanceForm.objects.filter(
                class_name=class_id,
                date__gte=start_date,
                date__lte=end_date
            )

            student_list = []
            for attendance_form in attendance_form_list:
                if attendance_form.student not in student_list:
                    student_list.append(attendance_form.student)

            attendance_data = {}
            for student in student_list:
                attendance_data[student] = [attendance_form.present for attendance_form in attendance_form_list.filter(student=student)]

            context['attendance_report'] = attendance_report
            context['attendance_data'] = attendance_data
            context['start_date'] = start_date
            context['end_date'] = end_date

        return context

class AttendanceReportDetailView(generic.DetailView):
    model = AttendanceReport
    template_name = 'attendance/attendance_report_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.object

        # Get the list of attendance objects associated with this report
        attendance_list = report.attendance.all()

        # Calculate the overall attendance percentage for this report
        total_students = report.attendance_form.class_object.students.count()
        present_students = attendance_list.filter(status='P').count()
        percentage = round(present_students / total_students * 100, 2)

        context['attendance_list'] = attendance_list
        context['percentage'] = percentage

        return context