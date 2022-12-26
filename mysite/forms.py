
from django import forms

class HomeForm(forms.Form):  

    selvalue_timeperiod = ( 
        ('Year-to-Year', 'Year-to-Year'),
        ('Month-to-Month', 'Month-to-Month'),
    )

    selvalue_startendyear = ( 
        ('1895', '1895'),
        ('1896', '1896'),
        ('1897', '1897'),
        ('1898', '1898'),
        ('2022', '2022'),
    )
    selvalue_portfolio = ( 
        ('巴菲特退休策略(Warren Buffett Retirement Plan)', '巴菲特退休策略(Warren Buffett Retirement Plan)'),
        ('永續投資策略(Permanent Portfolio)', '永續投資策略(Permanent Portfolio)'),
        ('全天候投資策略(All Weather Portfolio)', '全天候投資策略(All Weather Portfolio)'),
    )
    #author = forms.CharField()
    #timeperiod = forms.CharField(max_length=20,widget=forms.widgets.Select(choices=selvalue_timeperiod))
    #startyear = forms.CharField(max_length=4,widget=forms.widgets.Select(choices=selvalue_startendyear))
    #endyear = forms.CharField(max_length=4,widget=forms.widgets.Select(choices=selvalue_startendyear))
    initialamount = forms.CharField(label='起始投入金額$')  
    portfolio= forms.CharField(max_length=99,widget=forms.widgets.Select(choices=selvalue_portfolio))
    
