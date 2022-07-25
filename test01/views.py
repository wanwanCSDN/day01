from django.shortcuts import render, redirect
from test01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


# Create your views here.


# 靓号列表显示
def pretty_list(request):
    # 搜索框 将台input框数据传入value _data
    data_dict = {}
    value_data = request.GET.get('num', "")
    if value_data:
        data_dict["mobile__contains"] = value_data
    # 分页 从前台获取页码值
    page = int(request.GET.get("page", 1))
    page_size = 5
    start = (page - 1) * page_size
    end = page * page_size
    data_list = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[start:end]
    # 根据数据库生成页码

    data_num = models.PrettyNum.objects.filter(**data_dict).order_by("-level").count()
    # print(data_num)
    # page_num = int(data_num / 5)
    # print(page_num)

    # 用函数计算生成多少页码
    page_num, div = divmod(data_num, page_size)
    if div:
        page_num += 1
    # 判断页码极值 控制页码不产生负值以及超过总条数的分页数
    plus_page = 5
    if page_num <= plus_page * 2 + 1:
        start_page = 1
        end_page = page_num + 1
    else:
        if page <= plus_page:
            start_page = 1
            end_page = page * 2 + 1
        else:
            if (page + plus_page) > page_num:
                end_page = page_num
                start_page = page_num - 2 * plus_page
            else:
                start_page = page - plus_page
                end_page = page + plus_page + 1

    page_list = []
    # 上一页
    if page > 1:
        preve = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        preve = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_list.append(preve)

    for i in range(start_page, end_page):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_list.append(ele)

        # 下一页
    if page < page_num:
        preve = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        preve = '<li><a href="?page={}">下一页</a></li>'.format(page_num)
    page_list.append(preve)
    page_str = mark_safe("".join(page_list))
    print(page_str)




    return render(request, "pretty_list.html", {"data_list": data_list, "value_data": value_data, "page_str": page_str})


class PrettyModelForm(forms.ModelForm):
    # moible = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator()]
    # )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", 'price', 'status', 'level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        text_mobile = self.cleaned_data['mobile']
        exit = models.PrettyNum.objects.filter(mobile=text_mobile).exists()
        if len(text_mobile) != 11:
            raise ValidationError("格式错误")
        elif exit:
            raise ValidationError("手机号重复")
        else:
            return text_mobile


# 靓号列表新增
def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    else:
        return render(request, "pretty_add.html", {"form": form})


class PrettyEditModelForm(forms.ModelForm):
    # moible = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator()]
    # )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", 'price', 'status', 'level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        text_mobile = self.cleaned_data['mobile']
        exit = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=text_mobile).exists()
        if len(text_mobile) != 11:
            raise ValidationError("格式错误")
        elif exit:
            raise ValidationError("手机号重复")
        else:
            return text_mobile


# 编辑靓号
def pretty_eidt(request, nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, "pretty_edit.html", {"form": form})
    form = PrettyEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    else:
        return render(request, "pretty_edit.html", {"form": form})


# 删除
def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
