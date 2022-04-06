from django.db import models
from utlis.base_model import BaseModel


# Create your models here.


class Envs(BaseModel):
    id = models.AutoField(verbose_name="id主键", help_text="id主键", primary_key=True)
    name = models.CharField(verbose_name="环境名称", max_length=200, unique=True, help_text="环境名称")
    base_url = models.URLField(verbose_name="请求URL", max_length=200, help_text="请求URL")
    desc = models.CharField(verbose_name="简要描述", help_text="简要描述", max_length=200)

    class Meta:
        db_table = "tb_envs"
        verbose_name = "环境信息"
        verbose_name_plural = verbose_name


