from django.db import models
from utlis.base_model import BaseModel


# Create your models here.
class Reports(BaseModel):
    id = models.AutoField(verbose_name="id主键", help_text="id主键", primary_key=True)
    name = models.CharField(verbose_name="报告名称", help_text="报告名称", unique=True, max_length=200)
    result = models.BooleanField("执行结果", default=1, help_text="执行结果")
    count = models.IntegerField("用例总数", help_text="用例总数")
    success = models.IntegerField("成功总数", help_text="成功总数")
    html = models.TextField("测试报告HTML源码", help_text="测试报告HTML源码", null=True, blank=True)
    summary = models.TextField("报告详情", help_text="报告详情", null=True, blank=True, default="")

    class Meta:
        db_table = "tb_reports"
        verbose_name = "测试报告"
        verbose_name_plural = verbose_name
