from django.db import models


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=32)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)
    level_choice = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)
    status_choice = (
        (1, "占用"),
        (2, "未占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, default=2)
