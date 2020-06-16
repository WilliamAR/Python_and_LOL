import pandas as pd
import os

class OrganizarBase(object):
    
    def __init__(self):
        
        '''
        Llama a todas las bases de datos como una instancia.
        
        Las bases contienen: 
            Baneos, Oro, Asesinatos, Información de la partida, Monstruos y
            estructuras.
        
        Nota: Las bases dedeben estar contenidas en una carpeta llamada "data"
            
        Carga todas las bases suministradas de Kaggle del siguiente
            enlace https://www.kaggle.com/chuckephron/leagueoflegends/metadata 
            y modificados segúnla conveniencia de las gráficas o el tipo de 
            análisis.
        '''
        
    def baneo(self):
        
        '''
        Return:
            Base de datos que contiene el baneo durante las partidas.
        '''
        
        lol_bans = pd.read_csv(os.path.join('data','bans.csv'))
        
        return lol_bans
    
    def oro(self):
        
        '''
        Return:
            Base de datos que contiene el oro durante las partidas.
        '''
        
        lol_gold = pd.read_csv(os.path.join('data','gold.csv'))
        
        return lol_gold
    
    def muerte(self):
        
        '''
        Return:
            Base de datos que contiene las muertes durante las partidas.
        '''
        
        lol_kills = pd.read_csv(os.path.join('data','kills.csv'))
        
        return lol_kills
    
    def info_partida(self):
        
        '''
        Return:
            Base de datos que contiene la información general durante las 
            partidas.
        '''
        
        lol_match_info = pd.read_csv(os.path.join('data','matchinfo.csv'))
        
        return lol_match_info
    
    def monstruo(self):
        
        '''
        Return:
            Base de datos que contiene la ejecución de los monstruos durante 
            las partidas.
        '''
        
        lol_monsters = pd.read_csv(os.path.join('data','monsters.csv'))
        
        return lol_monsters
    
    def estructura(self):
        
        '''
        Return:
            Base de datos que contiene la ejecución de las estructuras durante 
            las partidas.
        '''
        
        lol_structures = pd.read_csv(os.path.join('data','structures.csv'))
        
        return lol_structures
    
    def arreglar_baneo(self, lol_bans):
        
        '''
        Parámetros:
            lol_bans: DataFrame que contiene los baneos de las partidas.

        Return:
            DataFrame con algunas correcciones en la información.
        '''
        
        lol_bans = lol_bans.set_index(
            ['Address', 'Team']).stack().reset_index().rename(
                columns = {0: 'Champion_ban', 'level_2': 'Number_ban', 
                            'Team': 'Team_ban'})
                
        return lol_bans
    
    def arreglar_oro(self, lol_gold):
        
        '''
        Parámetros:
            lol_gold: DataFrame que contiene el oro de las partidas.

        Return:
            DataFrame con algunas correcciones en la información.
        '''
        
        lol_gold = lol_gold.set_index(['Address','Type']).stack().\
            unstack(level = 'Type').reset_index().rename(
                columns = {'level_1':'Time_gold'})
            
        lol_gold.Time_gold = lol_gold.Time_gold.\
            str.replace(r'(min_)(.*)',r'\2').astype(int)
        
        lol_gold = lol_gold.drop(labels = ['goldblue', 'goldred', 'golddiff'],
                                 axis = 1)
                
        return lol_gold
    
    def arreglar_muerte(self, lol_kills):
        
        '''
        Parámetros:
            lol_kills: DataFrame que contiene las muertes en las partidas.

        Return:
            DataFrame con algunas correcciones en la información.
        '''
        
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
                
        return lol_kills
    
    def arreglar_monstruo(self, lol_monsters):
        
        '''
        Parámetros:
            lol_monsters: DataFrame que contiene las ejecuciones de los 
            monstruos en las partidas.

        Return:
            DataFrame con algunas correcciones en la información.
        '''
        
        lol_monsters = lol_monsters.rename(
            columns = {'Team': 'Team_monster', 'Time': 'Time_monster', 
                        'Type': 'Type_monster'})
                
        return lol_monsters
    
    def arreglar_estructura(self, lol_structures):
        
        '''
        Parámetros:
            lol_monsters: DataFrame que contiene las ejecuciones de los 
            monstruos en las partidas.

        Return:
            DataFrame con algunas correcciones en la información.
        '''
        
        lol_structures = lol_structures.rename(
            columns = {'Team': 'Team_structure', 'Time': 'Time_structure', 
                        'Type': 'Type_structure'})
                
        return lol_structures
    
    def base(self):
        
        '''
        Return:
            Devuelve todas las bases de League of Legends en DataFrame 
            separados.
        '''
        
        OB = OrganizarBase()
        b = OB.baneo()
        o = OB.oro()
        m = OB.muerte()
        ip = OB.info_partida()
        mo = OB.monstruo()
        e = OB.estructura()
        
        return b, o, m, ip, mo, e
        
        
    
    def arreglar_base(self):
        
        '''
        Return:
            Devuelve todas las bases de League of Legends en DataFrame 
            separados con las modificaciones prefijadas para cada DataFrame.
        '''
        OB = OrganizarBase()
        b, g, k, mi, m, s = OB.base()
        
        b = OB.arreglar_baneo(b)
        g = OB.arreglar_oro(g)
        k = OB.arreglar_muerte(k)
        m = OB.arreglar_monstruo(m)
        s = OB.arreglar_estructura(s)
        
        return b, g, k, mi, m, s
