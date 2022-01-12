############################################################  LIBRAIRIES  ################################################################
import streamlit as st
import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
#############################################################  WEBSCRAPPING  ##############################################################
token = { 'X-Auth-Token': '04e38b231f8c46a5a0b86aaba82a8437' }

#requetage principale data 1
@st.cache(persist = True)
def prp_data1():
    url = "http://api.football-data.org/v2/competitions/"
    response = requests.request("GET", url, headers = token)
    return response.json()

#requetage principale data 2
@st.cache(persist = True)
def prp_data2(param,compet,valeur):
    url = "http://api.football-data.org/v2/competitions/" + str(compet[valeur]) + "/" + param
    response = requests.request("GET", url, headers = token)
    return response.json()

def choixdeligue(choix,data):
    ligues = []
    for i in range(len(data['competitions'])):
        if(data['competitions'][i]['area']['name'] == choix):
            ligues.append(data['competitions'][i]['name'])
    for i in range(len(ligues)):
        st.subheader((ligues[i]))

#############################################################  TITRES, LIENS, IMAGE  ######################################################
st.title('TABLEAU DE BORD SUR LE FOOT')
st.sidebar.title('NAVIGATION')

image = Image.open('C:/Users/allak/Desktop/Datasets/Football/Foot_Macron.png')
st.image(image, output_format="PNG")

linkedin ='[Linkedin](https://www.linkedin.com/in/maxime-allakere-hormo-648409103/)'
github = '[Github](https://github.com/mallaker/PSB_X)'
st.sidebar.write('Vous pourrez consulter ce projet dans mon ' + github, ' et vous pourrez aussi me joindre sur mon ' + linkedin)

lienapi ='[Football-data](https://www.football-data.org/)'
with st.expander("Concernant cet tableau de bord"):
    st.write("Pour citer Pierre De Coubertin, historien et passioné de foot : « Un seul sport n'a connu ni arrêts ni reculs : le football. A quoi cela peut-il tenir sinon à la valeur intrinsèque du jeu lui-même, aux émotions qu'il procure, à l'intérêt qu'il présente ». Il s'agit d'un projet de visualisation autours d'une passion commune le foot. Visualisation des stats foot de tous les grands championnats dans certains pays. Le projet utilise un API fournit par " + lienapi,  " le site par reference pour le webscrapping des données foot ( Historique des matchs, des buts, stats des joeurs, scores en direct, matchs à venir, équipes, alignements / remplaçants, etc.)")



data1 = prp_data1()
stade = {}
compet = {}
for i in range(len(data1['competitions'])):
    stade[data1['competitions'][i]['area']['name']] = 0
    compet[data1['competitions'][i]['name']] = 0


for i in range(len(data1['competitions'])):
    stade[data1['competitions'][i]['area']['name']] += 1
    compet[data1['competitions'][i]['name']] += 1


stade_df = pd.DataFrame(stade.items(), columns=['Pays', 'Total'])
compet_df = pd.DataFrame(compet.items(), columns=['League Name','Count'])

################################################################  WORDCLOUD  ############################################################
wine_mask = np.array(Image.open('C:/Users/allak/Desktop/Datasets/Football/wine_mask.png'))
def transform_format(val):
    if val == 0:
        return 255
    else:
        return val

transformed_wine_mask = np.ndarray((wine_mask.shape[0],wine_mask.shape[1]), np.int32)

for i in range(len(wine_mask)):
    transformed_wine_mask[i] = list(map(transform_format, wine_mask[i]))

wordcloudnew = st.sidebar.button('Nouveau Wordcloud!',key = 1,)
wordcloudnew = True
if(wordcloudnew):
    mots = ' '.join(compet_df['League Name'])
    wordcloud = WordCloud(stopwords = STOPWORDS, max_words=1000, background_color = 'white',width = 820, height = 410,mask=transformed_wine_mask,contour_width=3, contour_color='firebrick').generate(mots)
    plt.figure(figsize=[20,10])
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.axis("off")
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.pyplot()

wordcloudnew = False

#############################################################  LES STATS GENERALES  ########################################################

st.sidebar.header('LES STATS GENERALES :\n')

compet_stats = st.sidebar.checkbox('Distribution par pays',key=None)

if(compet_stats):
    st.header('Nombre de compétitions par pays:\n')
    choix_pays = st.sidebar.multiselect('Choisir le pays',stade_df['Pays'],key = 1)
    if(len(choix_pays) == 0):
        st.write('Choisir le pays..')
    else:    
        sub_stade_df = stade_df[stade_df['Pays'].isin(choix_pays)].reset_index().drop(['index'],axis = 1)
        sub_stade_df.index = range(1,len(sub_stade_df) + 1)
        st.table(sub_stade_df)
        st.write('\n')
        if(sub_stade_df.shape[0] != 0):
            sns.set_style('whitegrid')
            params = {'legend.fontsize': 18,
                'figure.figsize': (20, 8),
                'axes.labelsize': 22,
                'axes.titlesize': 22,
                'xtick.labelsize': 22,
                'ytick.labelsize': 22,
                'figure.titlesize': 22}
            plt.rcParams.update(params)
            fig, ax = plt.subplots() 
            ax = sns.barplot(data = sub_stade_df,x = 'Pays',y = 'Total')
            if(len(sub_stade_df) > 5):
                plt.xticks(rotation = 60)
            if(len(sub_stade_df) > 10):
                plt.xticks(rotation = 90)
            sns.despine(left = True)
            st.pyplot(fig)  

champ_continent = st.sidebar.checkbox('Championnats de foot par continent',key=2)

continents = ['Europe','Asia','Africa','North America','South America','Australia']

if(champ_continent):
    choix = st.sidebar.radio('Choisir le continent',continents,key=2)
    write = choix + '\'s football leagues: '
    st.header(write + '\n')
    choixdeligue(choix,data1)

champ_pays = st.sidebar.checkbox('Championnats de foot par pays',key = 3)

if(champ_pays):
    helper = list(stade_df[~stade_df['Pays'].isin(continents)]['Pays'])
    choix = st.sidebar.selectbox('Choisir le pays',helper, key=3)
    write = choix + '\'s football leagues: '
    st.caption(write + '\n')
    choixdeligue(choix,data1)
    
##########################################################  LES STATS PAR COMPETITION  #########################################################

st.sidebar.header('LES STATS PAR COMPETITION :\n')

compet = {}
champ_list = ['Serie A','Premier','UEFA Champions','European','Ligue 1','Bundesliga','Eridivisie','Primeira Liga','Primera Division','FIFA World Cup']

for i in range(len(data1['competitions'])):
    if(data1['competitions'][i]['name'] not in champ_list):
        continue
    compet[data1['competitions'][i]['name']] = data1['competitions'][i]['id']

default = 'Choisir la Competition'
options = [default]

options = options + list(compet.keys())
valeur = st.sidebar.selectbox('',options,key = 4)

if(valeur != default):
    st.title(valeur)   
    if(st.sidebar.checkbox('Info equipe')):
        data2 =prp_data2("teams",compet,valeur)
        st.header('Nombre equipes: ' + str(data2['count']))
        col1, col2 = st.columns(2)
        if(len(data2['teams'])):
            for i in range(len(data2['teams'])):
                if(i % 2):
                    col1.subheader(data2['teams'][i]['name'])
                    if('address' in data2['teams'][i].keys()):
                        col1.write('Adresse: ' + data2['teams'][i]['address'])
                    if('phone' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['phone'] != None):
                            col1.write('Contact: ' + (data2['teams'][i]['phone']))
                    if('website' in data2['teams'][i].keys()):
                        col1.write('Site web: ' + data2['teams'][i]['website'])
                    if('email' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['email'] != None):
                            col1.write('Email: ' + data2['teams'][i]['email'])
                    if('founded ' in data2['teams'][i].keys()):
                        col1.write('Fondé en ' + str(data2['teams'][i]['founded']))
                    if('venue' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['venue'] != None):
                            col1.write('Stade: ' + data2['teams'][i]['venue'])
                else:
                    col2.subheader(data2['teams'][i]['name'])
                    if('address' in data2['teams'][i].keys()):
                        col2.write('Adresse: ' + data2['teams'][i]['address'])
                    if('phone' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['phone'] != None):
                            col2.write('Contact: ' + (data2['teams'][i]['phone']))
                    if('website' in data2['teams'][i].keys()):
                        col2.write('Site web: ' + data2['teams'][i]['website'])
                    if('email' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['email'] != None):
                            col2.write('Email: ' + data2['teams'][i]['email'])
                    if('founded' in data2['teams'][i].keys()):
                        col2.write('Fondé en ' + str(data2['teams'][i]['founded']))
                    if('venue' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['venue'] != None):
                            col2.write('Stade: ' + data2['teams'][i]['venue'])

    if(st.sidebar.checkbox('Classement stats')):
        st.header('Classement stats: ')
        data2 = prp_data2("standings",compet,valeur)
        if(valeur != 'FIFA World Cup'):
            type = st.sidebar.radio('',['Total']) 
            if(type == 'Total'):
                data3 = pd.DataFrame()
                for i in range(len(data2['standings'][0]['table'])):
                    list = []
                    list.append(data2['standings'][0]['table'][i]['position']) 
                    list.append(data2['standings'][0]['table'][i]['team']['name'])
                    list.append(data2['standings'][0]['table'][i]['playedGames']) 
                    list.append(data2['standings'][0]['table'][i]['form']) 
                    list.append(data2['standings'][0]['table'][i]['won']) 
                    list.append(data2['standings'][0]['table'][i]['lost']) 
                    list.append(data2['standings'][0]['table'][i]['points']) 
                    list.append(data2['standings'][0]['table'][i]['goalsFor']) 
                    list.append(data2['standings'][0]['table'][i]['goalsAgainst']) 
                    list.append(data2['standings'][0]['table'][i]['goalDifference'])
                    data3 = data3.append(pd.Series(list),ignore_index = True) 

            data3.drop([0],axis = 1,inplace = True)
            data3.columns = ['Equipe','Matchs joués','5 derniers matchs','Gagné','Perdu','Points','Buts normaux','Buts contre son camp','Difference']
            #data3.columns = ['Team Name','Matches Played','Last 5 Matches','Won','Lost','Points','Goals For','Goals Against','Difference']
            data3.index = range(1,len(data3) + 1)
            st.table(data3)
        else:
                for j in range(0,len(data2['standings']),3):
                    data3 = pd.DataFrame()
                    for i in range(len(data2['standings'][j]['table'])):
                        list = []
                        list.append(data2['standings'][j]['table'][i]['position']) 
                        list.append(data2['standings'][j]['table'][i]['team']['name'])
                        list.append(data2['standings'][j]['table'][i]['playedGames']) 
                        list.append(data2['standings'][j]['table'][i]['form']) 
                        list.append(data2['standings'][j]['table'][i]['won']) 
                        list.append(data2['standings'][j]['table'][i]['lost']) 
                        list.append(data2['standings'][j]['table'][i]['points']) 
                        list.append(data2['standings'][j]['table'][i]['goalsFor']) 
                        list.append(data2['standings'][j]['table'][i]['goalsAgainst']) 
                        list.append(data2['standings'][j]['table'][i]['goalDifference'])
                        data3 = data3.append(pd.Series(list),ignore_index = True) 
                    st.subheader(data2['standings'][j]['group'])
                    data3.drop([0],axis = 1,inplace = True)
                    data3.columns = ['Equipe','Matchs joués','5 derniers matchs','Gagné','Perdu','Points','Buts normaux','Buts contre son camp','Difference']
                    data3.index = range(1,len(data3) + 1)
                    st.table(data3)
    if(st.sidebar.checkbox('Buteurs')):
        data2 =prp_data2('scorers',compet,valeur)
        st.subheader('Top 10 buteurs:')
        data3 = pd.DataFrame()
        for i in range(len(data2['scorers'])):
            list = []
            list.append(data2['scorers'][i]['player']['name'])
            list.append(data2['scorers'][i]['player']['nationality'])
            list.append(data2['scorers'][i]['player']['position'])
            list.append(data2['scorers'][i]['team']['name'])
            list.append(data2['scorers'][i]['numberOfGoals'])
            data3 = data3.append(pd.Series(list),ignore_index = True)
        data3.index = range(1,len(data3) + 1)
        data3.columns = ['Nom','Nationalité','Position','Equipe','Nombre de buts']
        st.table(data3)

    if(st.sidebar.checkbox('Fiche Joueur')):
        data2 =prp_data2('scorers',compet,valeur)
        st.subheader('Fiche joueur:')
        data3 = pd.DataFrame()
        for i in range(len(data2['scorers'])):
            list = []
            list.append(data2['scorers'][i]['player']['name'])
            list.append(data2['scorers'][i]['player']['dateOfBirth'])
            list.append(data2['scorers'][i]['player']['countryOfBirth'])
            list.append(data2['scorers'][i]['player']['nationality'])
            list.append(data2['scorers'][i]['player']['position'])
            list.append(data2['scorers'][i]['player']['shirtNumber'])
            list.append(data2['scorers'][i]['team']['name'])
            data3 = data3.append(pd.Series(list),ignore_index = True)
        data3.index = range(1,len(data3) + 1)
        data3.columns = ['Nom','Date de Naissance','Pays de Naissance','Nationalité','Position','Numero','Equipe']
        st.table(data3)

############################################################  LES DATASETS  ############################################################
       
data2 = prp_data2("standings",compet,valeur)

data3 = pd.DataFrame()
for i in range(len(data2['standings'][0]['table'])):
    list = []
    list.append(data2['standings'][0]['table'][i]['position']) 
    list.append(data2['standings'][0]['table'][i]['team']['name'])
    list.append(data2['standings'][0]['table'][i]['playedGames']) 
    list.append(data2['standings'][0]['table'][i]['form']) 
    list.append(data2['standings'][0]['table'][i]['won']) 
    list.append(data2['standings'][0]['table'][i]['lost']) 
    list.append(data2['standings'][0]['table'][i]['points']) 
    list.append(data2['standings'][0]['table'][i]['goalsFor']) 
    list.append(data2['standings'][0]['table'][i]['goalsAgainst']) 
    list.append(data2['standings'][0]['table'][i]['goalDifference'])
    data3 = data3.append(pd.Series(list),ignore_index = True) 
data3.drop([0],axis = 1,inplace = True)
data3.columns = ['Equipe','Matchs joués','5 derniers matchs','Gagné','Perdu','Points','Buts normaux','Buts contre son camp','Difference']
data3.index = range(1,len(data3) + 1)
st.sidebar.header('LES DATASETS :\n')

default = 'Choisir la data'
options = [default]
list_data=['Premier jeu de données','Deuxieme jeu de données','Troisieme jeu de données']
options = options + list_data
valeur = st.sidebar.selectbox('',options,key =3)
st.header("Mon jeu de données selectionné :")
# for i in range (len(list_data)):
if (valeur=='Premier jeu de données'):
    st.write(data1)
elif (valeur=='Deuxieme jeu de données'):
    st.write(data2)
else : 
    st.table(data3)
