from django import forms
from apps.land.models import *


class LandInformationForm(forms.ModelForm):
    class Meta:
        model = LandInfo
        fields = ('title', 'content', 'desc', 'reward_price', 'information_source')


class TransInformationForm(forms.ModelForm):
    class Meta:
        model = TransInfo
        fields = ('title', 'content', 'desc', 'reward_price', 'information_source')


class AttractInformationForm(forms.ModelForm):
    class Meta:
        model = AttractInfo
        fields = ('title', 'content', 'desc', 'reward_price', 'information_source')


class ActivityInformationForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            'title', 'desc', 'content', 'activity_datetime', 'activity_place', 'information_source',
            'reward_price', 'traffic_tips', 'quota', 'content_feed'
        )


class PropertyInformationForm(forms.ModelForm):
    class Meta:
        model = PropertyList
        fields = ('title', 'content', 'desc', 'reward_price', 'information_source', 'file_introduction',)


class InvestmentInformationForm(forms.ModelForm):
    class Meta:
        model = InvestmentData
        fields = ('title', 'content', 'desc', 'reward_price', 'information_source', 'file_introduction',)


"""数据录入"""


class NoticeEntryForm(forms.ModelForm):
    class Meta:
        model = LandInfo
        fields = ('city', 'area', 'location', 'serial_number', 'advance_date',
                  'listed_date', 'transfer_date', 'land_nature', 'land_area', 'plot_ratio',
                  'greening', 'building_density', 'transfer_mode', 'margin', 'start_price',
                  'transfer_high_price', 'plan_condition', 'remark', 'c_f',
                  )


class TransEntryForm(forms.ModelForm):
    class Meta:
        model = TransInfo
        fields = ('city', 'area', 'location', 'serial_number',
                  'land_nature', 'land_area', 'plot_ratio',
                  'greening', 'building_density', 'trading_type', 'deposit', 'price',
                  'people', 'contact', 'plan_conditions', 'licensor', 'trading_conditions'
                  )


class AttractEntryForm(forms.ModelForm):
    class Meta:
        model = AttractInfo
        fields = ('city', 'area', 'location', 'serial_number',
                  'land_nature', 'land_area',
                  'notice_date', 'total_inv',
                  'people', 'contact', 'cooperate_condition'
                  )


class DealForm(forms.ModelForm):
    class Meta:
        model = LandInfo
        fields = ('serial_number', 'deal_time', 'deal_money', 'transferee_peo', 'deal_remark')


class InvChargeMergeForm(forms.ModelForm):
    class Meta:
        model = InvChargeMerge
        fields = ('city', 'area', 'location', 'serial_number',
                  'land_nature', 'land_area', 'plot_ratio',
                  'building_density', 'trading_type', 'deposit', 'price', 'deal_money', 'transferee_peo',
                  'licensor', 'plan_conditions', 'trading_conditions')


class BuildingSupplyForm(forms.ModelForm):
    class Meta:
        model = BuildingSupplyF
        fields = ('city', 'acreage', 'tao_num', 'year_month',)


class BuildingSupplyTForm(forms.ModelForm):
    class Meta:
        model = BuildingSupplyT
        fields = ('city', 'acreage', 'tao_num', 'deal_average', 'year_month')


class ValueBuildingForm(forms.ModelForm):
    class Meta:
        model = ValueBuilding
        fields = ('city', 'area', 'project_name', 'location',
                  'total_building_area', 'land_area', 'plot_ratio', 'total_tao',
                  'selling_tao', 'yitui_tao', 'in_average', 'selling_average',
                  'product_composition', 'h_area', 'supporting_business', 'supporting_education',
                  'traffic_conditions', 'developers', 'sales', 'first_time',
                  )


class TopInForm(forms.ModelForm):
    class Meta:
        model = Top_In
        fields = ('city', 'in_time', 'company_name', 'develop_project', 'new_ranking', 'headquarters_location',)


class BigDataForm(forms.ModelForm):
    class Meta:
        model = BigData
        fields = ('city', 'positioning', 'city_card', 'GDP', 'peo_num', 'pillar_industries', 'key_enterprises',
                  'development_plan', 'planning_for',)


class NoticeClientForm(forms.ModelForm):
    class Meta:
        model = LandInfo
        fields = ('city', 'area', 'location', 'serial_number', 'advance_date',
                  'listed_date', 'transfer_date', 'land_nature', 'land_area', 'plot_ratio',
                  'greening', 'building_density', 'transfer_mode', 'margin', 'start_price',
                  'transfer_high_price', 'plan_condition', 'remark', 'c_f', 'house_account',
                  'title', 'content', 'desc', 'yuji_guapai', 'now_progress', 'add_amplitude',
                  'special_requirements', 'reward_price', 'coordinates', 'pcc',
                  )


class TransClientForm(forms.ModelForm):
    class Meta:
        model = TransInfo
        fields = ('city', 'area', 'location', 'serial_number','coordinates',
                  'land_nature', 'land_area', 'plot_ratio', 'remark',
                  'greening', 'building_density', 'trading_type', 'deposit', 'price',
                  'people', 'contact', 'plan_conditions', 'licensor', 'trading_conditions','pcc',
                  'title', 'content', 'desc', 'house_account', 'information_validity', 'reward_price'
                  )


class AttractClientForm(forms.ModelForm):
    class Meta:
        model = AttractInfo
        fields = ('city', 'area', 'location', 'serial_number',
                  'land_nature', 'land_area', 'plot_ratio',
                  'notice_date', 'total_inv', 'house_account',
                  'people', 'contact', 'cooperate_condition','pcc',
                  'title', 'content', 'desc', 'remark', 'industry_requirements', 'reward_price','coordinates'
                  )
