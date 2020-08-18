import pandas as p
import numpy as np 
import re
import pickle
All_houses=[]
features=['du prix de','Parking','Placard','Sous-sol','prix','€/ mois','€ / m²','Pièces','Chambre','Année de construction','Indice d\'émission de gaz à effet de serre','Diagnostic de performance énergétique :','Ascenseur','Toilette','Cuisine','Salle de séjour','entrée','Cave','Vue','Gardien','Digicode','Salle de bain','Interphone',"Salle d\'eau",'Alarme','Calme','Parquet','Rangements',"Balcon"]

def searchFeatures(i,scrappedData:list,features:list):    
    house=dict()
    for item in scrappedData:
        feature=feature_is_item(features,scrappedData,item)        
        print(feature)
        data_split=feature.split('=>')
        house[data_split[0]]=data_split[1]
    try:
        house['type']=' '.join(scrappedData).split('Vente:')[1].split()[0]
        adresse=' '.join(scrappedData).split('Vente:')[1].split()
        house['adresse']=' '.join(adresse[3:adresse.index('-')])
        if(house.get('type')=='Studio'):
            adresse=' '.join(scrappedData).split('Vente:')[1].split()
            house['adresse']=' '.join(adresse[1:adresse.index('-')])

        house['surface']=re.findall('\d*,*\d*m²',' '.join(scrappedData).split('Vente:')[1])[0]
        house['link']='http'+house_strings[i].split('http')[1]  
    except :
        print('************************* probleme ****************************')

    print(house)
    All_houses.append(house)   

def feature_is_item(features:list,scrappedData:list,scrappedItem:str):
    feature_value=0
    for feature in features:#loop through features on scrappeditem
        if (feature in scrappedItem):#feature found
            print(feature)
            print("scrapped item : "+scrappedItem)
            
            #get feature value
            feature_value=scrappedItem.replace(feature,'').strip()
            #get feature value if not mentionned
            if(len(feature_value)==0):
                feature_value=str(1)
            print('feature value :'+feature_value)
            
            break
    return feature +'=>'+ str(feature_value)
        


with open('all_house-features.csv') as f:
    content=f.read()

content=str(content)

content=re.sub('[<>]','',content)

house_strings=content.split('#')

house_lists=[house[0:house.lower().find('https')].split(',') for house in house_strings]



searchFeatures(887,house_lists[887],features)
print(' \n')

print(house_lists[887])
print(' \n')
print(house_strings[887])



ind=0
for scrappedHouse in house_lists:
    searchFeatures(ind,scrappedHouse,features)
    ind+=1

for house in All_houses:
    if('pièces' in str(house.get('adresse'))):
            adress=re.sub('[\w\s]*pièces','',str(house.get('adresse')))                
            house['adresse']=adress
            print(adress)

with open('All_houses.pickle','wb') as f:
    pickle.dump(All_houses,f)

print(ind)
print('\n\n')
print(All_houses[1])
print('\n\n')
print(All_houses[2])


#df=p.DataFrame(data=All_houses,columns=feats)
#print(df)

