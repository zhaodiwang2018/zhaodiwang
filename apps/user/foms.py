from django import forms
from apps.user.models import *


class SelfEditForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('job', 'company', 'addr', 'address_scale', 'username',
                  'plot_ratio', 'invest_pattern', 'land_nature', 'city', 'area')


class EditForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('job', 'company', 'addr', 'username', 'city', 'area', 'intro')
