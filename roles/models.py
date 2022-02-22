from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField
from shop.models import Item
# Create your models here.


class BaseModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BusinessPerson(BaseModel):
    class BusinessType(models.TextChoices):
        PUBLISHING = 'PUB', _('Books')
        FARMING = 'FAR', _('Food')
        TAILORING = 'TAI', _('Fabric Material')
        CONSTRUCTION = 'CON', _('Construction Materials')
        TIMBER = 'TIM', _('Timber')
        METALS = 'MET', _('Metal')
        CHEMICALS = 'CHE', _('Oils')
        HERBS = 'HER', _('Herbs')
    # what are his/her business details? => (Business Details)
    business_type = models.CharField(max_length=50, choices=BusinessType.choices,
                                     default=BusinessType.TIMBER)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    business_description = models.TextField(max_length=1024)
    location = models.CharField(max_length=255, null=True, blank=True)
    # what are his/her personal details? => (Personal Details)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    confirm_password = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(blank=True)
    # next of kin details (in case we cannot reach the business man) => (Next of Kin Details)
    next_of_kin_name = models.CharField(max_length=255, null=True, blank=True)
    next_of_kin_email = models.EmailField(null=True, blank=True)
    next_of_kin_contact = PhoneNumberField(blank=True)
    # what does he/she sell? => (Product Details)
    items = models.ManyToManyField(Item)
    # how long has it taken before the goods got sold? => (Analysis Parameters)
    date_sold = models.DateTimeField(null=True, blank=True)

    # what are his/her account details? => (Account Details)
    class PaymentMode(models.TextChoices):
        MPESA = 'MPESA', _('Mpesa')
        BANK = 'BANK', _('Bank Account')
    preferred_payment_mode = models.CharField(max_length=50, choices=BusinessType.choices,
                                              default=PaymentMode.MPESA)
    bank_account_number = models.CharField(
        max_length=50, null=True, blank=True)
    bank_code = models.CharField(max_length=255, null=True)
    mpesa_till_number = models.CharField(max_length=10, null=True, blank=True)
    mpesa_pay_bill_number = models.CharField(
        max_length=10, null=True, blank=True)

    # place him/her in the registry.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.business_name}-{self.first_name}"


class Teacher(BaseModel):
    # what are his/her personal details? => (Personal Details)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=1024)
    confirm_password = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField()
    location = models.CharField(max_length=255, null=True, blank=True)
    # what is his/her salary details?
    salary = models.IntegerField(null=True, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)

    # analysis parameters
    probation = models.BooleanField(default=False)

    # place him/her in the registry.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name


class Class(BaseModel):
    class ClassCategory(models.TextChoices):
        BUSINESS = 'BUS', _('Business')
        FARMING = 'FAR', _('Farming')
        TAILORING = 'TAI', _('Tailoring')
        CONSTRUCTIONWORK = 'CON', _('Construction Work')
        WOODWORK = 'WOO', _('Wood Work')
        METALWORK = 'MET', _('Metal Work')
        COOKING = 'COO', _('Cooking')
        CHEMICAL_MIXING = 'CHE', _('Oils and Soap Making')
        NATURAL_REMEDIES = 'NAT', _('Healing and Herbal Mixing')
    # what are the class details? => (Class Details)
    class_category = models.CharField(max_length=50, choices=ClassCategory.choices,
                                      default=ClassCategory.FARMING)
    name = models.CharField(max_length=255, null=True, blank=True)

    # who is teaching the class? => (Teachers Details)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True
    )
    # assignment details
    assignment = models.FileField(null=True, blank=True)
    assignment_deadline = models.DateTimeField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    # analysis parameters
    started_time = models.DateTimeField(null=True, blank=True)
    ending_time = models.DateTimeField(null=True, blank=True)
    understood = models.BooleanField(default=False)
    need_repeat = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Student(BaseModel):
    class TypeOptions(models.TextChoices):
        WORKSTUDY = 'WS', _('Work Study')
        SELFSPONSORED = 'SSP', _('Self Sponsored')

    # what are his/her personal details?
    student_type = models.CharField(max_length=50, choices=TypeOptions.choices,
                                    default=TypeOptions.WORKSTUDY)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=1024)
    confirm_password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=200, null=True)

    # what class is this student in and who is his teacher?
    student_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, null=True, blank=True
    )

    # place him/her in the registry
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    # analysis parameter
    completed_assignment = models.BooleanField(default=False)
    probation = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
