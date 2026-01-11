from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from projects.models import Project

class ProjectStageUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stage_updates')
    stage_number = models.PositiveSmallIntegerField()  # 1 to 7
    stage_name = models.CharField(max_length=100,  blank= True , null= True )
    stage_description = models.TextField( blank= True , null= True )
    completion_percentage = models.PositiveSmallIntegerField( blank= True , null= True )  
    field_image = models.ImageField(upload_to='stage_images/' ,  blank= True , null= True )
    report_pdf = models.FileField(upload_to='stage_reports/' ,  blank= True , null= True )
    remaining_cost = models.DecimalField(max_digits=15, decimal_places=2)  
    remaining_duration = models.CharField(max_length=100) 
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['stage_number']
        verbose_name = "تحديث مرحلة مشروع"
        verbose_name_plural = "تحديثات مراحل المشاريع"

    def clean(self):
        if self.stage_number < 1 or self.stage_number > 7:
            raise ValidationError("رقم المرحلة يجب أن يكون بين 1 و 7.")

        
        if self.remaining_cost >= self.project.estimated_cost:
            raise ValidationError("الكلفة المتبقية يجب أن تكون أقل من الكلفة الكلية للمشروع.")

        
        last_update = ProjectStageUpdate.objects.filter(
            project=self.project,
            stage_number=self.stage_number - 1
        ).first()
        if last_update and self.remaining_cost >= last_update.remaining_cost:
            raise ValidationError("الكلفة المتبقية يجب أن تكون أقل من القيمة السابقة.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
