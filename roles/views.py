from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View, generic

from roles.models import Class, Student, Teacher
from users.models import User

from .forms import (
    BusinessRegistrationForm,
    ClassRegistrationForm,
    StudentRegistrationForm,
    TeacherRegistrationForm,
)


class TeacherRegistration(View):
    form_class = TeacherRegistrationForm
    initial = {"key": "value"}
    template_name = "roles/form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = User()
            user.username = form.cleaned_data.get("email")
            user.email = form.cleaned_data.get("email")
            user.password = make_password(form.cleaned_data.get("password"))
            user.is_teacher = True
            user.save()
            messages.success(
                request,
                "Successfully registered as one of the Country Livers Industrial "
                + "Training Institute Teachers",
            )
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {"form": form})


class TeacherListView(generic.ListView):
    template_name = "roles/list.html"
    queryset = Teacher.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = "teacher"
        context["object_list"] = self.queryset
        return context


class BusinessRegistration(View):
    form_class = BusinessRegistrationForm
    initial = {"key": "value"}
    template_name = "roles/form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = User()
            user.username = form.cleaned_data.get("email")
            user.email = form.cleaned_data.get("email")
            user.password = make_password(form.cleaned_data.get("password"))
            user.is_business = True
            user.save()
            messages.success(
                request,
                "You have successfully registered your business with "
                + "country livers",
            )
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {"form": form})


class ClassRegistration(View):
    form_class = ClassRegistrationForm
    initial = {"key": "value"}
    template_name = "roles/form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully added a class")
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {"form": form})


class ClassListView(generic.ListView):
    template_name = "roles/list.html"
    queryset = Class.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = "class"
        context["object_list"] = self.queryset
        return context


class ClassDetailView(generic.DetailView):
    template_name = "roles/detail.html"
    queryset = Class.objects.all()


class StudentRegistration(View):
    form_class = StudentRegistrationForm
    initial = {"key": "value"}
    template_name = "roles/form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = User()
            user.username = form.cleaned_data.get("email")
            user.email = form.cleaned_data.get("email")
            user.password = make_password(form.cleaned_data.get("password"))
            user.is_student = True
            user.save()
            messages.success(
                request,
                "You have successfully registered as a student of the Country"
                + " Living Training Institute",
            )
            return HttpResponseRedirect("/")

        return render(request, self.template_name, {"form": form})


class StudentListView(generic.ListView):
    template_name = "roles/list.html"
    queryset = Student.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = "student"
        context["object_list"] = self.queryset
        return context


class StudentDetailView(generic.DetailView):
    template_name = "roles/detail.html"
    queryset = Student.objects.all()


Teacher_registration = TeacherRegistration.as_view()
Class_registration = ClassRegistration.as_view()
Student_registration = StudentRegistration.as_view()
