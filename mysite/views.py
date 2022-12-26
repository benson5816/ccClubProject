from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic import TemplateView
from .forms import HomeForm

from pathlib import Path
import os

class HomeView(TemplateView):  
    #指定這個view對應到的顯示網頁
    template_name = 'home.html'
    template_name1 = 'homeOut.html'

    def get(self, request):    
        print('Enter get')
        form = HomeForm()    
        return render( request, self.template_name, {'form':form})  

    def post(self, request):  
        print('Enter post')
        form = HomeForm(request.POST) 
        if form.is_valid():
            #再抓取form裏的參數值
            #author = form.cleaned_data['author']   
            #timeperiod = form.cleaned_data['timeperiod']
            #startyear = form.cleaned_data['startyear']
            #endyear = form.cleaned_data['endyear']
            initialamount = form.cleaned_data['initialamount']
            portfolio = form.cleaned_data['portfolio']
        else:
            print('Not valid form')

    


        #pip install pandas
        import pandas as pd
        
        if portfolio=='巴菲特退休策略(Warren Buffett Retirement Plan)':
            ETFList = ['SPY','TLT']
            WeightList=[.9,.1]
        elif portfolio=='永續投資策略(Permanent Portfolio)':
            ETFList = ['VTI','TLT','GLD','SHY']
            WeightList=[.25,.25,.25,.25]
        elif portfolio=='全天候投資策略(All Weather Portfolio)':
            ETFList = ['VTI','TLT','IEF','GLD','DBC']
            WeightList=[.3,.4,.15,.075,.075]
        
        #資料下載
        #pip install yfinance
        import yfinance as yf
        dfAll = pd.DataFrame()
        for ETF in ETFList:
            df = yf.download(ETF, group_by="Ticker", period='max')
            df[ETF]=df['Adj Close']
            dfAll= pd.concat([dfAll,df[[ETF]]],axis=1)
            
            
        #報酬計算
        dfAll.sort_index(inplace=True)
        for ETF in ETFList:
            dfAll[ETF]=dfAll[ETF].pct_change()
        dfAll.dropna(inplace=True)
        dfAll['Portfolio']=0
        for ETF,Weight in zip(ETFList,WeightList):
            dfAll['Portfolio']=dfAll['Portfolio']+dfAll[ETF]*Weight
        
        
        #產生回測報表
        # 需下載git並安裝 https://git-scm.com/download/win
        #pip install git+https://github.com/quantopian/pyfolio
        import pyfolio as pf
        f=pf.create_returns_tear_sheet(dfAll['Portfolio'],return_fig=True )
        f.savefig(Path.cwd().joinpath('static' , 'returns.png'))
        import numpy as np
        from PIL import Image
        def bbox(im):
            a = np.array(im)[:,:,:3]  # keep RGB only
            m = np.any(a != [255, 255, 255], axis=2)
            coords = np.argwhere(m)
            y0, x0, y1, x1 = *np.min(coords, axis=0), *np.max(coords, axis=0)
            return (x0, y0, x1+1, y1+1)
        im = Image.open(Path.cwd().joinpath('static' , 'returns.png'))
        print(bbox(im))  # (33, 12, 223, 80)
        im2 = im.crop(bbox(im))
        im2.save(Path.cwd().joinpath('static' , 'returns.png'))
        
        a=pf.show_perf_stats(dfAll['Portfolio'] )
        b=pf.show_worst_drawdown_periods(dfAll['Portfolio'] )
         
        #write html to file
        text_file = open(Path.cwd().joinpath("templates","stat.html"), "w")
        text_file.write(a.to_html())
        text_file.write(b.to_html())
        text_file.close()

        #最終網頁整合至homeOut.html
        os.chdir(Path.cwd().joinpath("templates"))
        os.system("type home.html stat.html homePng.html > homeOut.html")
        os.chdir("..")

        finalValue= float(initialamount)*float((a.iloc[1,0]).strip('%'))/100 
        
        #計算時間
        import datetime as dt 
        start_date =dt.date(int(str(dfAll.index[0])[0:4]), int(str(dfAll.index[0])[5:7]), int(str(dfAll.index[0])[8:10]))
        last_date =dt.date(int(str(dfAll.index[-1])[0:4]), int(str(dfAll.index[-1])[5:7]), int(str(dfAll.index[-1])[8:10]))

        #計算時間，經過時間以年月日呈現
        #from dateutil.relativedelta import relativedelta
        #diff = relativedelta(last_date,start_date)
        #MyText='你選擇了『'+portfolio+'』的投資策略，你投資的'+str(format(int(initialamount),","))+'元從'+str(start_date)+'開始投資經過約'+str(diff.years)+'年'+str(diff.months)+'月'+str(diff.days)+'日，將成為'+str(format(int(finalValue),","))+'元，總報酬為'+a.iloc[1,0]+' (年化報酬為'+a.iloc[0,0]+')，更多詳情請參考下圖。'

        dif_days = (last_date - start_date).days
        dif_years = round(dif_days / 365, 2)
        MyText='你選擇了『'+portfolio+'』的投資策略，你投資的'+str(format(int(initialamount),","))+'元從'+str(start_date)+'開始投資經過約'+str(dif_years)+'年，將成為'+str(format(int(finalValue),","))+'元，總報酬為'+a.iloc[1,0]+' (年化報酬為'+a.iloc[0,0]+')，更多詳情請參考下圖。'
        
        print(MyText)

        args = {'form': form, 
                #'author': author,
                #'timeperiod': timeperiod, 
                #'startyear': startyear, 
                #'endyear': endyear,
                'initialamount': initialamount,
                'portfolio':portfolio,
                'MyText':MyText}  
    
        return render(request, self.template_name1, args)




