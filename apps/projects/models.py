from django.db import models
from utlis.base_model import BaseModel


# Create your models here.


class Projects(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name="id主键", help_text="id主键" )
    name = models.CharField("项目名称", max_length=200, unique=True, help_text="项目名称")
    leader = models.CharField("负责人", max_length=50, help_text="负责人")
    tester = models.CharField("测试人员", max_length=50, help_text="测试人员")
    programmer = models.CharField("开发人员", max_length=50, help_text="开发人员")
    publish_app = models.CharField("发布应用", max_length=100, help_text="发布应用")
    desc = models.CharField("简要描述", max_length=200, null=True, blank=True, default="", help_text="简要描述")

    class Meta:
        db_table = "tb_projects"
        verbose_name = "项目信息表"
        verbose_name_plural = verbose_name
