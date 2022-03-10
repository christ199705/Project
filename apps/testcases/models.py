from django.db import models
from utlis.base_model import BaseModel


# Create your models here.

class Testcases(BaseModel):
    id = models.AutoField(verbose_name="id主键", primary_key=True, help_text="id主键")
    name = models.CharField("用例名称", max_length=100, unique=True, help_text="用例名称")
    interfaces = models.ForeignKey("interfaces.Interfaces", on_delete=models.CASCADE, help_text="所属接口")
    include = models.TextField("前置", null=True, help_text="用例执行前置顺序")
    author = models.CharField("编写人员", max_length=50, help_text="编写人员")
    request = models.TextField("请求信息", help_text="请求信息")

    class Meta:
        ab_table = "tb_testcases"
        verbose_name = "用例信息"
        verbose_name_plural = verbose_name