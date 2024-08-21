from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# educational stage
EDUCAIONAL_STAGE = (
    ('Bakalavr', "Bakalavr"),
    ("O'qishni ko'chirish", "O'qishni ko'chirish"),
)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(BaseModel):
    telegram_id = models.PositiveBigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=128, null=True)

    def __str__(self):
        return f"{self.full_name} {self.username}"

    class Meta:
        db_table = "telegram_users"


class BotAdmin(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            pass
        super(BotAdmin, self).save(*args, **kwargs)
        
    class Meta:
        db_table = "bot_admins"
        

class Speciality(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    is_internal = models.BooleanField(default=False, verbose_name="Kunduzgi talabalar uchun mavjudmi")
    period_internal = models.PositiveIntegerField(verbose_name="O'qish muddati", null=True, blank=True, validators=[MinValueValidator(3), MaxValueValidator(6)])
    contract_price_internal = models.PositiveIntegerField(verbose_name="Kontrakt narxi", default=0)
    is_external = models.BooleanField(default=False, verbose_name="Sirtqi talabalar uchun mavjudmi")
    period_external = models.PositiveIntegerField(verbose_name="O'qish muddati", null=True, blank=True, validators=[MinValueValidator(3), MaxValueValidator(6)])
    contract_price_external = models.PositiveIntegerField(verbose_name="Kontrakt narxi", default=0)
    
    def __str__(self):
        return f"{self.name}"
    
    def get_contract_price(self, is_internal):
        if is_internal:
            return self.contract_price_internal
        return self.contract_price_external
    
    def get_periot(self, is_internal):
        if is_internal:
            return self.period_internal
        return self.period_external

    class Meta:
        db_table = "specialities"
        
        
class Contract(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    passport = models.CharField(max_length=20)
    birthday = models.CharField(max_length=50, null=True, blank=True)
    edu_stage = models.CharField(max_length=50, choices=EDUCAIONAL_STAGE, default="Bakalavr")
    is_internal = models.BooleanField(default=False)
    is_external = models.BooleanField(default=False)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    transkrip = models.ImageField(upload_to="transkrips", null=True, blank=True)
    semester = models.PositiveIntegerField(default=1, validators=[MinValueValidator(3), MaxValueValidator(8)])
    contract = models.FileField(upload_to="contract", null=True, blank=True)
    
    @property
    def edu_type(self):
        if self.is_internal:
            return "Kunduzgi"
        return "Sirtqi"
    
    def __str__(self):
        return f"{self.user} {self.speciality}"