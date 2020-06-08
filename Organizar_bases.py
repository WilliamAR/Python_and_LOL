import pandas as pd

class OrganizarBase(object):
    
    def __init__(self):
        
        '''
        Llama a todas las bases de datos como una instancia.
        
        Las bases contienen: 
            Baneos, Oro, Asesinatos, Información de la partida, Monstruos y
            estructuras.
        '''
    
    def arreglar_base(self):
        
        '''
        arreglar_base()
        
        Return:
            Carga todas las bases suministradas de Kaggle del siguiente
            enlace https://www.kaggle.com/chuckephron/leagueoflegends/metadata 
            y modificados segúnla conveniencia de las gráficas o el tipo de 
            análisis.
        '''
        
        #Base de datos bans
        lol_bans = pd.read_csv('bans.csv')
        
        #Base de datos oro
        lol_gold = pd.read_csv('gold.csv')
        
        #Base ded datos muertes
        lol_kills = pd.read_csv('kills.csv')
        
        #Base de datos, información
        #lol_LOL = pd.read_csv('LeagueofLegends.csv')
        
        #Base de datos información de la partida
        lol_match_info = pd.read_csv('matchinfo.csv')
        
        #Base de datos monstruos
        lol_monsters = pd.read_csv('monsters.csv')
        
        #Base de datos estructuras
        lol_structures = pd.read_csv('structures.csv')
            
        ## ORGANIZAR LA BASE BANS!!
        lol_bans = lol_bans.set_index(
            ['Address', 'Team']).stack().reset_index().rename(
                columns = {0: 'Champion_ban', 'level_2': 'Number_ban', 
                            'Team': 'Team_ban'})
        
        ## ORGANIZAR LA BASE GOLD!!
        lol_gold= lol_gold.set_index(['Address','Type']).stack().\
            unstack(level = 'Type').reset_index().rename(
                columns = {'level_1':'Time_gold'})
            
        lol_gold.Time_gold = lol_gold.Time_gold.\
            str.replace(r'(.*_)(.*)', r'\2').astype(int)
        lol_gold = lol_gold.drop(labels = ['goldblue', 'goldred', 'golddiff'],
                                 axis = 1)
        
        ## ORGANIZAR LA BASE KILLS!!
        lol_kills = lol_kills.set_index(
            ['Address','Team', 'Time', 'x_pos', 'y_pos']).stack().reset_index().\
            rename(
                columns = {'Team': 'Team_kill', 
                            'Time':'Time_kill', 
                            'level_5': 'Type_kill',
                            0: 'Player'})
        lol_kills.loc[~lol_kills.x_pos.str.isdigit(), 'x_pos'] = '0'
        lol_kills.loc[~lol_kills.y_pos.str.isdigit(), 'y_pos'] = '0'
        
        lol_kills.x_pos = lol_kills.x_pos.astype(int)
        lol_kills.y_pos = lol_kills.y_pos.astype(int)
        
        lol_kills.Player = lol_kills.Player.str.replace(r'(.*\s)(.*)', r'\2')
        
        ## ORGANIZAR LA BASE MONSTERS!!
        lol_monsters = lol_monsters.rename(
            columns = {'Team': 'Team_monster', 'Time': 'Time_monster', 
                        'Type': 'Type_monster'})
        
        ## ORGANIZAR LA BASE STRUCTURES!!
        lol_structures = lol_structures.rename(
            columns = {'Team': 'Team_structure', 'Time': 'Time_structure', 
                        'Type': 'Type_structure'})
        
        return lol_bans, lol_gold, lol_kills, lol_match_info, lol_monsters, lol_structures




