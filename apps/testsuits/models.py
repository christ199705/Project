from django.db import models
from utlis.base_model import BaseModel


# Create your models here.
class Testsuits(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name="id主键", help_text="id主键")
    name = models.CharField("套件名称", max_length=200, unique=True, help_text="套件名称")
    project = models.ForeignKey("projects.Projects", on_delete=models.CASCADE, help_text="所属项目")
    # 接口ID
    include = models.TextField("包含的接口", null=False, help_text="包含的接口")

    class Meta:
        db_table = "tb_testsuits"
        verbose_name = "套件信息"
        verbose_name_plural = verbose_name

