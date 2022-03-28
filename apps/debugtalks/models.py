from django.db import models
from utlis.base_model import BaseModel


# Create your models here.

class DebugTalks(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name="id主键", help_text="id主键")
    name = models.CharField("debugtalk文件名称", max_length=200, default="debugtalk.py", help_text="debugtalk文件名称")
    # python源代码，
    debugtalk = models.TextField(null=False, default="#debugtalk.py", help_text="debugtalk.py文件")
    project = models.OneToOneField("projects.Projects", on_delete=models.CASCADE, related_name="debugtalks",
                                   help_text="所属项目")


    class Meta:
        db_table = "tb_debugtalks"
        verbose_name = "debugtalk.py文件"
        verbose_name = verbose_name
