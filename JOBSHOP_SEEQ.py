# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 22:38:09 2021

@author: MONSTER
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
import matplotlib.font_manager as font_manager
from datetime import datetime




def RandomDegerAta(machines,jobs,min_t,max_t):
    matris=pd.DataFrame(columns=machines,index=jobs)
    x=0
    y=0
    while x<len(jobs):
        
        y=0
        while y<len(machines):
            matris.iloc[x,y]=np.random.randint(min_t, max_t)   #random sayı yerleştir    
            y+=1
        x+=1    
    return matris
 

   
def min_first_machine(data,makinalar): # STEP 1
    data_copy=data.copy()
    first_col=data.iloc[0::,0:1] # ilk kolon
    last_col=data.iloc[0::,-1::] # son kolon
    
    data_copy=data_copy.drop(axis=1,columns=data.columns[0])
    data_copy=data_copy.drop(axis=1,columns=data.columns[len(makinalar)-1])

    
    mid_matris=data.iloc[0::,1:len(makinalar)-1] #0.satırdan itibaren sonuna kadar - baştan 1 sonraki ve sondan 1 önceki kolonlar
    min_first_col=(first_col.min(axis=0)).min(axis=0) # ilk kolonun min değeri
    min_last_col=(last_col.min(axis=0)).min(axis=0)# son kolonun min değeri
    max_mid_matris=(mid_matris.max(axis=0)) # ortada kalan kolonların max değeri
    #print("min M1=",min_first_col," min_last=",min_last_col," mid max=",max_mid_matris)
    x=0
    condition1=False
    condition2=False
    while x<len(max_mid_matris):
        if(min_first_col>=max_mid_matris[x]):
            condition1=True
        if(min_last_col>=max_mid_matris[x]):
            condition2=True    
        x+=1
        
    condition=False
    if(condition1 or condition2):
        condition=True   
    return condition,min_first_col,min_last_col,max_mid_matris

def TwoMachineMatrix(cond): #STEP 2
    if(cond):
        mac=['G','H']
        GH=pd.DataFrame(index=isler,columns=mac)
        
        x=0
        z=0
        while z<len(mac):
            if(z==0):
            
                x=0
                while x<len(isler):
                    y=0
                    sumG=0
                    while y<len(makinalar)-1: # son makinayı almayacak
                        sumG+=MJ.iloc[x,y]
                        y+=1
                    
                    GH.iloc[x,z]=sumG               
                    
                    x+=1
            else:
                x=0
                while x<len(isler):
                    y=1
                    sumG=0
                    while y<len(makinalar): # ilk makinayı almayacak
                        sumG+=MJ.iloc[x,y]
                        y+=1
                    
                    GH.iloc[x,z]=sumG               
                    
                    x+=1
                
            z+=1
        
    else:
        print('ÇÖZÜM YOKTUR')
    return GH   

def minGHMatris(matris):
    i=0
    sıra=0
    job=0
    minValue=matris.iloc[0,0]
    while i<len(matris):
        j=0
        while j<2:
            if(minValue>matris.iloc[i,j]):
                minValue=matris.iloc[i,j]
                sıra=j
                job=i
            j+=1
        i+=1
    return minValue,job,sıra
    
    
# STEP 3 ---- oluşan GH matrisinde matrisin minimumunu bul. G de ise ilk başta
#H da ise en sona yazılır. Bunlara ayrı liste yap. BAŞ ve SON sonra birleştir. SON u tersten birleştir.
# Her  seçilen JOB tan sonra bulunduğu satır DROP olacak ana matriste (GH da)
# GH elemanı 0 adet kalıncaya kadar devam while(lenGH!=0) 

def TersListe(firstList,lastList):    
    i=0
    boy=len(lastList)
    while i<len(lastList):
        firstList.append(lastList[boy-1-i])
        i+=1        
    return firstList   

def MatrisGanttSınır(makina,jobs,matris): #matrisin toplam süresini hesapla
    i=0
    summary=0
    while i<len(jobs):
        j=0
        while j<len(makina):
            summary+=matris.iloc[i,j]
            j+=1
        i+=1
        
    return summary


def GantSureHesapla(matris,jobSequence,makinalar):
    i=0
    m_time1=0
    times=[]
    machineTime=[]
    processTime=[]
    MachineTicksForGantt=[]
    IDLETIME=[]
    S_POINT=[]#işin bittiği nokta GANT fonksyonu için
    
    idleSUM=0
    while i<len(makinalar): # makinaları sırasıyla işleme al
        #timeLine=[]
        j=0
        m_time1=0
        times=[]# yeni
        idleTime=[]
        StartPoint=[]#işin başladığı nokta GANT fonksyonu için
        prTime=[]#işin süresi
        makesPan=0
        while j<len(jobSequence): # iş öncelik sıralamasına göre
            startedJob=matris.index.get_loc(jobSequence[j]) # sıralamadaki işin kaçıncı satırda olduğunu bul indis olarak ver
            
            if(i>0): # ilk makinadan sonra 
                if(j==0): # başlanacak ilk iş ise                    
                    m_time1=matris.iloc[startedJob,i]+machineTime[i-1][j] # işe ait makinanın süresi (m1,m2,m3,m4...)
                    times.append(m_time1)
                    idleTime.append(0)# aylak zaman
                    StartPoint.append(machineTime[i-1][j])# başlangıç noktası/süresi
                    prTime.append(matris.iloc[startedJob,i]) # proses süresi
                    makesPan=m_time1
                else:# ilk işten sonraki işler
                    if(machineTime[i-1][j]>times[j-1]): # önceki makinanın şuanki iş adımının süresi > şuanki makinanın önceki iş süresinden büyükse
                        m_time1=matris.iloc[startedJob,i]+machineTime[i-1][j] #önceki makina ne zaman biterse o zaman yeni iş başlar + time
                       # idleTime.append(machineTime[i-1][j]-matris.iloc[startedJob,i]) # aradaki boşluk bekleme süresidir
                        idleTime.append(machineTime[i-1][j]-times[j-1]) 
                        idleSUM+=machineTime[i-1][j]-times[j-1]
                        times.append(m_time1)
                        StartPoint.append(machineTime[i-1][j])# başlangıç noktası aylak zamandan sonra StartPoint.append(machineTime[i-1][j]+idleT)
                        prTime.append(matris.iloc[startedJob,i])
                        makesPan=m_time1
                    else: #iş süresi önceki makinaın süresinden büyükse
                        m_time1=matris.iloc[startedJob,i]+times[j-1] # mevcut makinanın işi bittikten sonra başlar
                        idleTime.append(0)
                        makesPan=m_time1
                        times.append(m_time1)
                        StartPoint.append(times[j-1])
                        prTime.append(matris.iloc[startedJob,i])
                        
            else: # ilk makina ise 
                StartPoint.append(m_time1)
                m_time1+=matris.iloc[startedJob,i] # işe ait makinanın süresi (m1,m2,m3,m4...) MJ tablosu
                times.append(m_time1)  
                idleTime.append(0)
                makesPan=m_time1
                prTime.append(matris.iloc[startedJob,i])
            
            j+=1
        IDLETIME.append(idleTime)    
        machineTime.append(times) 
        MachineTicksForGantt.append(i+1)
        S_POINT.append(StartPoint)
        processTime.append(prTime)
        i+=1
    return machineTime,IDLETIME,idleSUM,times,MachineTicksForGantt,S_POINT,processTime,makesPan



def GANTT_SET_POINTS(StartPointList,ProcessTimeList,JobCount): # GANT için başlangıç nktası ve süre listesini hazırlar
    POINTS=[]
    lll=[(),()]
    a=0
    while a<len(StartPointList):
        b=0
        lll=[]
        while b<len(JobCount):
            lll.append((StartPointList[a][b],ProcessTimeList[a][b]))
            b+=1
        POINTS.append(lll)
        a+=1    
    return POINTS #liste dönderir

def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

def GANTT_GRAFIK_CIZ(makinalar,JobSequence,isler,GanttPoints,MJ,mTicksForGantt,StartPoint,ProcPoint,makesPan,GrafikTipi):
    
    clr=['red','green','blue','pink','orange','purple'] # isteğe bağlı renk listesi
    renkler=[]
    for name,hex in matplotlib.colors.cnames.items(): # renkler listesi
        renkler.append(hex)
    birimKare=makesPan/(len(makinalar)*len(JobSequence))    # gant karelerinin boyutu
    fig,gantt=plt.subplots()
    i=0
    while i<len(makinalar): 
        j=0
        while j<len(JobSequence):
            gantt.broken_barh([GanttPoints[i][j]],(i,1),facecolors=str(renkler[(j+5)*3])) #facecolors=str(clr[j]
            plt.text(StartPoint[i][j]+ProcPoint[i][j]/2, (0.5+i),JobSequence[j],fontsize='small') # bar üzerine LABEL yazdırma (başlangıçNoktası,yükseklik,Label,boyut)
            #sPT[i][j]+prPT[i][j]/2 > başlangıcNoktası + prosesSüresi/2 ile bar çubuğunun orta noktası belirlendi
            plt.text(StartPoint[i][j]+ProcPoint[i][j]-birimKare, (0.05+i),StartPoint[i][j]+ProcPoint[i][j],fontsize='small',color=str('lime')) # işlem süreleri ve makespan
            j+=1
        
   
        i+=1
    gantt.set_ylim(0,len(makinalar))
   #gantt.set_xlim(0,MatrisGanttSınır(makinalar, isler,MJ))
    gantt.set_xlim(0,makesPan) # gant sınır çizgisi
    gantt.set_xlabel(str(GrafikTipi))# 'zaman'
    gantt.set_ylabel('makinalar')
    #gantt.set_yticks([1,2,3,4,5])
    gantt.set_yticks(mTicksForGantt)
    gantt.set_yticklabels(makinalar)
    gantt.grid(True)    
    bilgi=font_manager.FontProperties(size='larger')
    gantt.legend(loc=1,prop=bilgi)
    
    now=datetime.now()
    tarih=now.strftime('%d%m%Y%H%M%S')       
    plt.savefig(str(GrafikTipi)+str(tarih))    
    plt.show()

def UYGUNLUK_TEST(makinalarListesi,JobListesi,Matris,minTime,maxTime):# Random matris oluşturup deneme yapılır
    Uygun=False
    iteras=0
    while Uygun!=True:    
        MJ=RandomDegerAta(makinalar,isler,minTime,maxTime) #
        Uygun,a,b,c=min_first_machine(MJ,makinalar)
        iteras+=1
        print(iteras,str(Uygun))
    return Uygun,MJ

def UYGUNLUK_TEST_XLSX(makinalarListesi,JobListesi,Matris): #dosyadan veri alınacaksa bu fonksyondan test yapılmalı
    Uygun=False
    iteras=0
    while Uygun!=True: # şartları TRUE verene kadar    iterasyon yap 
        MJ=Matris #
        Uygun,a,b,c=min_first_machine(MJ,makinalar)
        iteras+=1
        print(iteras,str(Uygun))
    return Uygun,MJ

def RANDOM_TERMIN_OLUSTUR(JobList,min_term,max_term):
    i=0
    deadline=[]
    while i<len(JobList):
        x=np.random.randint(min_term,max_term)
        deadline.append(x)
        i+=1
    return deadline

def SIRALA_KUCUK_BUYUK(Liste):
    i=1
    y=0
    t=0
    new_list=Liste.copy()
    indeksler=[]
    
    while t<len(Liste):
        indeksler.append(t)
        t+=1
    
   
    while y<len(Liste)-1:
        i=y+1
        while i<len(new_list):
            if(new_list[y]>new_list[i]): # ilk eleman , diğer elemandan büyükse 
               x=new_list[y] # ilk elemanı yedekle büyük olanı
               new_list[y]=new_list[i] # ilk eleman (küçük olacak) yeni değeri kendisinden küçük olan
               new_list[i]=x # küçük elemanın yerinide büyük eleman alacak
               ndx=indeksler[y]
               indeksler[y]=indeksler[i]
               indeksler[i]=ndx
            #else:indeksler[i]=y
            i+=1
        y+=1
    return new_list,indeksler

def SIRALA_TERMINE_GORE(DeadlineList,JobList):
    i=0    
    sortedList=[]
    while i<len(JobList):
        sortedList.append(JobList[DeadlineList[i]])
        i+=1
    return sortedList    

def IDLE_BY_MACHINE(TimeList,DataFrameIdle,index):
    i=0
    machineIdleList=[]
    while i<len(TimeList):
        machineIdleList.append(sum(TimeList[i]))
        DataFrameIdle.iloc[index,i]=sum(TimeList[i])
        i+=1
    #return DataFrameIdle        
#-----------------------
#TÜMLEŞİK KOD ÇALIŞMASI

makinalar=['M1','M2','M3','M4'] #makinalar=['M1','M2','M3','M4','M5','M6','M7']
isler=['J1','J2','J3','J4','J5','J6','J7','J8','J9','J10']#%isler=['J1','J2','J3','J4','J5','J6','J7','J8','J9','J10','J1X','J2X','J3x','J4X']
MJ=pd.DataFrame(columns=makinalar,index=isler)
Possible=False
Possible,MJ=UYGUNLUK_TEST(makinalar, isler, MJ,1,24)#6 ile 24 arasında random değerli matris oluşturur ve bu matrisi test eder. Sonuc TRUE olur ise JOBSHOP çalışır
if Possible==True:
    manuelYedek=MJ.copy()    
    cond,m1,m,mx=min_first_machine(MJ,makinalar)    
    GH=TwoMachineMatrix(cond)
    yedekGH=GH.copy()
    firstJob=[]
    lastJob=[]
    DeadLine=[]
    while GH.size!=0:
        minGH,job,sıra=minGHMatris(GH)
        
        if(sıra==1):
            lastJob.append(GH.index[job])
            GH=GH.drop(axis=0,index=GH.index[job])
        if(sıra==0):
            firstJob.append(GH.index[job])
            GH=GH.drop(axis=0,index=GH.index[job])
    
    DeadLine=RANDOM_TERMIN_OLUSTUR(isler,10,90) # işler için rastgele termin oluştur
    DeadLine_Sequence,DeadLine_Index=SIRALA_KUCUK_BUYUK(DeadLine) # termine göre küçükten büyüğe sıralama yapar ve hangi indexlerin değiştiğini verir
    DeadLine_JobSequence=SIRALA_TERMINE_GORE(DeadLine_Index, isler) # sıralanmış indexlerin karşılığını iş listesinde yapar verir
    
    JobSequence=TersListe(firstJob,lastJob) #ilk ve son listeleri birleştrp İŞ SIRALAMASI oluşturur
    MatrisGanttSınır(makinalar, isler,MJ)
    mTime=[]
    iTime=[]
    Times=[]
    mTicksForGantt=[]
    sPT=[]
    prPT=[]
    GanttPoints=[]
    MAKESPAN=0
    iSUM=0
    mTime,iTime,iSUM,Times,mTicksForGantt,sPT,prPT,MAKESPAN=GantSureHesapla(MJ,JobSequence,makinalar)
    GanttPoints=GANTT_SET_POINTS(sPT,prPT,JobSequence)
    GANTT_GRAFIK_CIZ(makinalar, JobSequence, isler, GanttPoints, MJ, mTicksForGantt, sPT,prPT,MAKESPAN,'JobShop')
    
    # ORJİNAL SIRALAMAYA GÖRE OLUŞACAK MAKESPAN
    MatrisGanttSınır(makinalar, isler,manuelYedek) # eski matrisi veriyoruz, son sınır zamanını belirliyor
    mTime_X=[]
    iTime_X=[]
    Times_X=[]
    mTicksForGantt_X=[]
    sPT_X=[]
    prPT_X=[]
    GanttPoint_X=[]
    MAKESPAN_X=0
    iSUM_X=0
    mTime_X,iTime_X,iSUM_X,Times_X,mTicksForGantt_X,sPT_X,prPT_X,MAKESPAN_X=GantSureHesapla(manuelYedek,isler,makinalar)
    GanttPoints_X=GANTT_SET_POINTS(sPT_X,prPT_X,isler)
    GANTT_GRAFIK_CIZ(makinalar, isler, isler, GanttPoints_X, manuelYedek, mTicksForGantt_X, sPT_X,prPT_X,MAKESPAN_X,'Normal Sıra')
    
    MatrisGanttSınır(makinalar, DeadLine_JobSequence,manuelYedek) # Termine göre sıralamalı işler ile ilerlemesi durumunda
    mTime_D=[]
    iTime_D=[]
    Times_D=[]
    mTicksForGantt_D=[]
    sPT_D=[]
    prPT_D=[]
    GanttPoints_D=[]
    MAKESPAN_D=0
    iSUM_D=0
    mTime_D,iTime_D,iSUM_D,Times_D,mTicksForGantt_D,sPT_D,prPT_D,MAKESPAN_D=GantSureHesapla(manuelYedek,DeadLine_JobSequence,makinalar)
    GanttPoints_D=GANTT_SET_POINTS(sPT_D,prPT_D,DeadLine_JobSequence)
    GANTT_GRAFIK_CIZ(makinalar, DeadLine_JobSequence, DeadLine_JobSequence, GanttPoints_D, manuelYedek, mTicksForGantt_D, sPT_D,prPT_D,MAKESPAN_D,'Termine Göre')

    #3 farklı uygulamanın karşılaştırılması
    SummaryTable=pd.DataFrame(columns=['JobShop','DeadlineSorted','NormalJobSorted'],index=['Makespan','IdleTime'])
    SummaryTable.iloc[0,0]=MAKESPAN
    SummaryTable.iloc[0,1]=MAKESPAN_X
    SummaryTable.iloc[0,2]=MAKESPAN_D
    SummaryTable.iloc[1,0]=iSUM
    SummaryTable.iloc[1,1]=iSUM_X
    SummaryTable.iloc[1,2]=iSUM_D
    
    SummaryIdleByMachine=pd.DataFrame(columns=makinalar,index=['JobShop','DeadlineSorted','NormalJobSorted'])
    IDLE_BY_MACHINE(iTime, SummaryIdleByMachine, 0) # JobShop yönteminde makina Aylak zamanları > SummaryIdleByMachine tablosuna işler
    IDLE_BY_MACHINE(iTime_D, SummaryIdleByMachine, 1) # Termin sıralaması yönteminde makina Aylak zamanları > SummaryIdleByMachine tablosuna işler
    IDLE_BY_MACHINE(iTime_X, SummaryIdleByMachine, 2)# Normal iş sıralama yönteminde makina Aylak zamanları > SummaryIdleByMachine tablosuna işler
    
    ax=SummaryTable.plot.bar(rot=0) # Makespan kıyaslama grafiği
    idle_ax=SummaryIdleByMachine.plot.bar(rot=0) # Makina boş zaman-yöntem grafiği
    

else:
    print('MATRİS OLUŞMADI !')


#---------------SON--------------------------

def EXCELDEN_DATA_GANT(dataBook,makinalar,isler,MJ):
    makinalar=[]
    isler=[]  
    MJ=pd.DataFrame(data=None)      
    dataBook=pd.read_excel("JobShopData.xlsx",sheet_name="Data",index_col=0)
    makinalar=dataBook.columns
    isler=dataBook.index
    MJ=dataBook.copy()
    Possible=False
    Possible,MJ=UYGUNLUK_TEST_XLSX(makinalar, isler, MJ)
    if Possible==True:
        manuelYedek=MJ.copy()    
        cond,m1,m,mx=min_first_machine(MJ,makinalar)    
        GH=TwoMachineMatrix(cond)
        yedekGH=GH.copy()
        firstJob=[]
        lastJob=[]
        DeadLine=[]
        while GH.size!=0:
            minGH,job,sıra=minGHMatris(GH)
            
            if(sıra==1):
                lastJob.append(GH.index[job])
                GH=GH.drop(axis=0,index=GH.index[job])
            if(sıra==0):
                firstJob.append(GH.index[job])
                GH=GH.drop(axis=0,index=GH.index[job])
        
        DeadLine=RANDOM_TERMIN_OLUSTUR(isler,10,90) # işler için rastgele termin oluştur
        DeadLine_Sequence,DeadLine_Index=SIRALA_KUCUK_BUYUK(DeadLine) # termine göre küçükten büyüğe sıralama yapar ve hangi indexlerin değiştiğini verir
        DeadLine_JobSequence=SIRALA_TERMINE_GORE(DeadLine_Index, isler) # sıralanmış indexlerin karşılığını iş listesinde yapar verir
        
        JobSequence=TersListe(firstJob,lastJob) #ilk ve son listeleri birleştrp tek liste yapar
        MatrisGanttSınır(makinalar, isler,MJ)
        mTime=[]
        iTime=[]
        Times=[]
        mTicksForGantt=[]
        sPT=[]
        prPT=[]
        GanttPoints=[]
        MAKESPAN=0
        iSUM=0
        mTime,iTime,iSUM,Times,mTicksForGantt,sPT,prPT,MAKESPAN=GantSureHesapla(MJ,JobSequence,makinalar)
        GanttPoints=GANTT_SET_POINTS(sPT,prPT,JobSequence)
        GANTT_GRAFIK_CIZ(makinalar, JobSequence, isler, GanttPoints, MJ, mTicksForGantt, sPT,prPT,MAKESPAN,'JobShop')
        
        # ORJİNAL SIRALAMAYA GÖRE OLUŞACAK MAKESPAN
        MatrisGanttSınır(makinalar, isler,manuelYedek) # eski matrisi veriyoruz, son sınır zamanını belirliyor
        mTime_X=[]
        iTime_X=[]
        Times_X=[]
        mTicksForGantt_X=[]
        sPT_X=[]
        prPT_X=[]
        GanttPoint_X=[]
        MAKESPAN_X=0
        iSUM_X=0
        mTime_X,iTime_X,iSUM_X,Times_X,mTicksForGantt_X,sPT_X,prPT_X,MAKESPAN_X=GantSureHesapla(manuelYedek,isler,makinalar)
        GanttPoints_X=GANTT_SET_POINTS(sPT_X,prPT_X,isler)
        GANTT_GRAFIK_CIZ(makinalar, isler, isler, GanttPoints_X, manuelYedek, mTicksForGantt_X, sPT_X,prPT_X,MAKESPAN_X,'Normal Sıra')
        
        MatrisGanttSınır(makinalar, DeadLine_JobSequence,manuelYedek) # eski matrisi veriyoruz, son sınır zamanını belirliyor
        mTime_D=[]
        iTime_D=[]
        Times_D=[]
        mTicksForGantt_D=[]
        sPT_D=[]
        prPT_D=[]
        GanttPoints_D=[]
        MAKESPAN_D=0
        iSUM_D=0
        mTime_D,iTime_D,iSUM_D,Times_D,mTicksForGantt_D,sPT_D,prPT_D,MAKESPAN_D=GantSureHesapla(manuelYedek,DeadLine_JobSequence,makinalar)
        GanttPoints_D=GANTT_SET_POINTS(sPT_D,prPT_D,DeadLine_JobSequence)
        GANTT_GRAFIK_CIZ(makinalar, DeadLine_JobSequence, DeadLine_JobSequence, GanttPoints_D, manuelYedek, mTicksForGantt_D, sPT_D,prPT_D,MAKESPAN_D,'Termine Göre')
    
        #3 farklı uygulamanın karşılaştırılması
        SummaryTable=pd.DataFrame(columns=['JobShop','DeadlineSorted','NormalJobSorted'],index=['Makespan','IdleTime'])
        SummaryTable.iloc[0,0]=MAKESPAN
        SummaryTable.iloc[0,1]=MAKESPAN_X
        SummaryTable.iloc[0,2]=MAKESPAN_D
        SummaryTable.iloc[1,0]=iSUM
        SummaryTable.iloc[1,1]=iSUM_X
        SummaryTable.iloc[1,2]=iSUM_D
        
        SummaryIdleByMachine=pd.DataFrame(columns=makinalar,index=['JobShop','DeadlineSorted','NormalJobSorted'])
        IDLE_BY_MACHINE(iTime, SummaryIdleByMachine, 0) # JobShop yönteminde makina Aylak zamanları > SummaryIdleByMachine tablosuna işler
        IDLE_BY_MACHINE(iTime_D, SummaryIdleByMachine, 1) # Termin sıralaması yönteminde makina Aylak zamanları > SummaryIdleByMachine tablosuna işler
        IDLE_BY_MACHINE(iTime_X, SummaryIdleByMachine, 2)# Normal iş sıralama yönteminde makina Aylak zamanları > SummaryIdleByMachine tablosuna işler
        
        ax=SummaryTable.plot.bar(rot=0) # Makespan kıyaslama grafiği
        idle_ax=SummaryIdleByMachine.plot.bar(rot=0) # Makina boş zaman-yöntem grafiği
        
    
    else:
        print('MATRİS OLUŞMADI !')
    


#------------------------EXCEL DATA ------------------
dataBook=pd.read_excel("JobShopData.xlsx",sheet_name="Data",index_col=0)
makinalar=dataBook.columns
isler=dataBook.index
MJ=dataBook
EXCELDEN_DATA_GANT(dataBook,makinalar,isler,MJ)

#-------------------------------------------
kume=[5,2,3,6,1]
kume2,sorted_index=SIRALA_KUCUK_BUYUK(kume)
ddd=[]
ddd[0]=0
len(iTime)
sum(iTime_D[3])

#----------------------------------------------------------------
renkler=[]
renkadi={}
renkkodu={}
rgb_renkkodu={}
for name,hex in matplotlib.colors.cnames.items():
    renkler.append(hex)
    renkadi[name]=hex
    renkkodu[hex]=name
    rgb_renkkodu[name]=matplotlib.colors.to_rgb(hex)

#---------------GANT EKLENECEK FORMUL




#♦-----------------------------------

GanttPoints[4][1]

renkler[0]
renkadi['aqua']
renkkodu['#F0F8FF']
GH=yedekGH
GH.size
len(GH)
GH.iloc[1,1]
min2matrix=GH.index.min(axis=0)
min2matrix=GH.index.min()
GH.columns.get_loc('G')
GH.index[1]
GH.columns[0]

x=np.random.randint(3,10)  
first_col=MJ.iloc[0::,0:1]
mid_matris=MJ.iloc[0::,1:len(makinalar)-1]
max_midmatris=mid_matris.max(axis=0)

max_midmatris[1]
data_copy=MJ.drop(axis=1,columns=MJ.columns[len(makinalar)-1])
data_copy=data_copy.drop(axis=1,columns=MJ.columns[0])
data_copy.max
len(MJ)
