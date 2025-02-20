import pandas as pd 
import numpy as np 
import os

DATA_FOLDER= "data"
file_under500=os.path.join(DATA_FOLDER,r"under500.csv")
file_over500= os.path.join(DATA_FOLDER,r"over500.csv")

# Load dataset, dataset is ready
df_under500=pd.read_csv(filepath_or_buffer=file_under500)
df_over500=pd.read_csv(filepath_or_buffer=file_over500)

df_under500['slab']=df_under500['start'].astype('str')+"-"+df_under500['end'].astype('str')
df_under500=df_under500.set_index('slab')

df_over500['slab']=df_over500['start'].astype('str')+"-"+df_over500['end'].astype('str')
df_over500=df_over500.set_index('slab')
df_over500


def compute_slabwise_consumption(*,units_consumed:int,df:pd.DataFrame):
    slabmarkers=df["start"].tolist()
    slabmarkers.append(np.inf)


    #calculate the splt

    remaining=units_consumed
    # [0-100: 100, 100-200: 100, 100-400: 100]
    D={}
    i=0
    L=[]
    for curr_slab,start,end in zip(df.index,df.start,df.end):
        end=np.float64(end)
        start=np.float64(start)

        consumed_by_slab=min(remaining,end-start)
        L.append(consumed_by_slab)
        remaining-=consumed_by_slab


        i+=1
    
    df["myunits"]=L
    
def compute_slabwise_price(*,df:pd.DataFrame):
     df["myunits_price"]=df["rate"]*df["myunits"]

def calculate_bill(units_consumed):
    if units_consumed<=500:
        df=df_under500.copy()
        #print("units_consumed<500, so Using under500 slab")
    else:
        df=df_over500.copy()
        #print("units_consumed>500, so Using over500 slab")

    

    compute_slabwise_consumption(units_consumed=units_consumed,df=df)
    compute_slabwise_price(df=df)


    return {'amount':int(df["myunits_price"].sum()),'df':df,"units_consumed":units_consumed}



import matplotlib.pyplot as plt 
import seaborn as sns


#sns.lineplot(data=precomputed_lookup_table)
#plt.show()




# given a price, determine units consumed

