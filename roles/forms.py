from django import forms
from django.forms import ModelForm
from django import forms

from roles.models import BusinessPerson
from .models import (Teacher, Class, Student)


class TeacherRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        exclude = ['user', 'salary', 'date_joined', 'probation']

    def clean(self):
        """
        checks whether the passwords match
        """
        data = self.cleaned_data
        if data.get("password") != data.get("confirm_password"):
            self.add_error("confirm_password", "passwords do not match !")
        return data


class SalaryForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'salary',
            'date_joined'
        ]


class TeacherProbationForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'probation'
        ]


class ClassRegistrationForm(ModelForm):
    class Meta:
        model = Class
        exclude = [
            'user',
            'understood',
            'need_repeat',
            'assignment',
            'assignment_deadline',
            'date_completed',
            'started_time',
            'ending_time',
        ]


class ClassAssignmentForm(ModelForm):
    class Meta:
        model = Class
        fields = [
            'assignment',
            'assignment_deadline',
            'date_completed'
        ]


class ClassAnalysisForm(ModelForm):
    class Meta:
        model = Class
        fields = [
            'started_time',
            'ending_time',
            'understood',
            'need_repeat'
        ]


class StudentRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        exclude = ['user', 'completed_assignment', 'probation']

    def clean(self):
        """
        checks whether the passwords match
        """
        data = self.cleaned_data
        if data.get("password") != data.get("confirm_password"):
            self.add_error("confirm_password", "passwords do not match !")
        return data


class StudentAssignmentCompletionForm(ModelForm):

    class Meta:
        model = Student
        fields = ['completed_assignment']


class StudentProbationForm(ModelForm):
    class Meta:
        model = Student
        fields = ['probation']


class BusinessRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = BusinessPerson
        fields = [
            'business_type', 'business_name',
            'business_description', 'location',
            'first_name', 'middle_name',
            'last_name', 'email',
            'phone_number'
        ]

    def clean(self):
        """
        checks whether the passwords match
        """
        data = self.cleaned_data
        if data.get("password") != data.get("confirm_password"):
            self.add_error("confirm_password", "passwords do not match !")
        return data


class NextOfKinForm(ModelForm):
    class Meta:
        model = BusinessPerson
        fields = [
            'next_of_kin_name',
            'next_of_kin_email',
            'next_of_kin_contact'
        ]


class AccountDetails(ModelForm):
    class Meta:
        model = BusinessPerson
        fields = [
            'preferred_payment_mode',
            'bank_account_number',
            'bank_code',
            'mpesa_till_number',
            'mpesa_pay_bill_number'
        ]
