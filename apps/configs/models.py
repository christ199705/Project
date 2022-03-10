from django.db import models

# Create your models here.
from utlis.base_model import BaseModel


class Configs(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name="id主键", help_text="id主键")
    name = models.CharField("配置名称", max_length=50, help_text="配置名称")
    interfaces = models.ForeignKey("interfaces.Interfaces", on_delete=models.CASCADE, related_name="configs",
                                   help_text="所属接口")
    author = models.CharField("编写人员", max_length=50, help_text="编写人员")
    request = models.TextField("请求信息", help_text="请求信息")

    class Meta:
        db_table = "tb_configs"
        verbose_name = "配置信息"
        verbose_name_plural = verbose_name
