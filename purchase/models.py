from django.db import models
from django.utils import timezone
from account.models import Profile
from django.core.validators import FileExtensionValidator
from django.db import transaction


class PurchaseType(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вид закупки"
        verbose_name_plural = "Виды закупок"
        db_table = "purchase_type"


class Purchase(models.Model):
    purchase_type = models.ForeignKey(to=PurchaseType, on_delete=models.CASCADE, verbose_name="Вид закупки")
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name="Профиль")
    number = models.CharField(verbose_name="Номер закупки", max_length=300, blank=True, unique=True, editable=False)
    title = models.CharField(verbose_name="Название закупки", max_length=255)
    text = models.TextField(verbose_name="Текст", blank=True, null=True)
    documentation = models.FileField(verbose_name="Документация", upload_to="files/documentation/%Y/%m/%d/", validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])], blank=True, null=True)
    contract = models.FileField(verbose_name="Договор", upload_to="files/contract/%Y/%m/%d/", validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])], blank=True, null=True)
    tech_task =models.FileField(verbose_name="Техническое задание", upload_to="files/tech_task/%Y/%m/%d/", validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])], blank=True, null=True)
    instruction = models.FileField(verbose_name="Инструкция", upload_to="files/instruction/%Y/%m/%d/", validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])], blank=True, null=True)
    winner = models.CharField(verbose_name="Победитель", max_length=255, blank=True, null=True)
    date_start = models.DateTimeField(verbose_name="Дата подачи", auto_now_add=True, editable=False)
    date_end = models.DateTimeField(verbose_name="Дата конца")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.number:
            today_date = timezone.now().strftime("%d_%m_%Y")
            last_purchase = Purchase.objects.order_by('-date_start').first()
            if last_purchase:
                last_number = int(last_purchase.number.split("_")[-1])
                new_number = f"{today_date}_{last_number + 1:02d}"
            else:
                new_number = f"{today_date}_01"
            self.number = new_number

        with transaction.atomic():
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Закупка"
        verbose_name_plural = "Закупки"
        db_table = "purchase"


class PurchaseMember(models.Model):
    purchase = models.ForeignKey(to=Purchase, on_delete=models.CASCADE, verbose_name="Закупка", blank=True, related_name="purchase_members")
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name="Профиль", related_name="purchase_member")
    status = models.CharField(verbose_name="Статус", blank=True, default="В ожидании")
    queue = models.PositiveBigIntegerField(verbose_name="Очередь", blank=True, unique=True)

    def __str__(self):
        return self.purchase.title + " - " + str(self.profile)

    class Meta:
        verbose_name = "Участник закупки"
        verbose_name_plural = "Участники закупки"
        db_table = "purchase_members"


class PurchaseAdditional(models.Model):
    purchase = models.ForeignKey(to=Purchase, on_delete=models.CASCADE, verbose_name="Закупка", blank=True, related_name="purchase_additional")
    qualification = models.CharField(verbose_name="Квалификация", max_length=255)
    requirement = models.CharField(verbose_name="Требования", max_length=255)

    def __str__(self):
        return self.qualification + " --- " + self.requirement
    
    class Meta:
        verbose_name = "Квалификация и требования"
        verbose_name_plural = "Квалификации и требования"
        db_table = "purchase_additional"


class LegalAct(models.Model):
    title = models.CharField(verbose_name="Тема", max_length=255)
    file = models.FileField(verbose_name="Файл", upload_to="files/legal-act/", validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])], blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Нормативно-правовой акт"
        verbose_name_plural = "Нормативно-правовые акты"
        ordering = ["id"]
        db_table = "legal_act"


class ContactInfo(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=5000)
    text = models.TextField(verbose_name="Описание")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактные информации"
        db_table = "contact_info"