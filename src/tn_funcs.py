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


def __compute_slabwise_consumption(*,units_consumed:int,df:pd.DataFrame):
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
    
def __compute_slabwise_price(*,df:pd.DataFrame):
     df["myunits_price"]=df["rate"]*df["myunits"]

def calculate_bill(units_consumed):
    if units_consumed<=500:
        df=df_under500.copy()
        #print("units_consumed<500, so Using under500 slab")
    else:
        df=df_over500.copy()
        #print("units_consumed>500, so Using over500 slab")

    

    __compute_slabwise_consumption(units_consumed=units_consumed,df=df)
    __compute_slabwise_price(df=df)


    return {'amount':int(df["myunits_price"].sum()),'df':df,"units_consumed":units_consumed}



import matplotlib.pyplot as plt 
import seaborn as sns


#sns.lineplot(data=precomputed_lookup_table)
#plt.show()




# given a price, determine units consumed

## Reverse lookup---------------------------------------------------

#CONFIG
filename=os.path.join(DATA_FOLDER,r"processed/precomputed_ltable_unitsconsumed_price.csv")

#Auto
def __load_reverse_ltable(filename):


    df=pd.read_csv(filepath_or_buffer=filename)
    data_inverted = df.to_dict(orient="list") 
    data_inverted= dict(zip(df["value"],df["key"]))
    return data_inverted


data_inverted=__load_reverse_ltable(filename)


def determine_units_using_billAmount(price):
    def __determine_border_prices(L:list,x:int): 
        '''almost like binary search'''
        low=0
        high=len(L)-1

        i=0
        while (low<high and i<200):
            print(f"boundary {low} to {high}")
            i+=1

            mid=int((low+high)/2)
            if x==L[mid]:
                break
            elif x>L[mid]:
                
                low=mid
            
            else:
                high=mid

            if low+1==high:
                break
               
        print(f"boundary {low} to {high}")
        low=low
        high=high#int(np.round(high))
        print (L[low],L[high])
        return (L[low],L[high])

    def __determine_corresponding_border_units(lowerindex,upperindex,data_inverted):
        lowerprice=data_inverted[lowerindex]
        upperprice=data_inverted[upperindex]

        return lowerprice,upperprice

    def __linear_interpolation(x,z1,z2):
        x1,y1=z1
        x2,y2=z2
        return y1 + (x - x1) / (x2 - x1) * (y2 - y1)

 
    lowerprice,upperprice=__determine_border_prices(list(data_inverted.keys()),price)
    lowerunits,upperunits=__determine_corresponding_border_units(lowerprice,upperprice,data_inverted)

    esti_units=__linear_interpolation(price,(lowerprice,lowerunits),(upperprice,upperunits))
    
    return int(esti_units)
