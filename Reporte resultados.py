import pandas as pd
from Organizar_bases import OrganizarBase
from Graficas_generales import (GraficaGeneralBaneo, GraficaGeneralOro,
                                GraficaGeneralMuerte, GraficaGeneralMonstruo,
                                GraficaGeneralEstructura)
from Save_Images import AlmacenarImagen

l = OrganizarBase()
a,b,c,d,e,f = l.arreglar_base()



x = GraficaGeneralBaneo()

nombres_campeones = x.nombres(
    base_lol = a, 
    lon_nombres = 6, 
    columna = 'Champion_ban')

top_n_baneo = x.top_n(
    base_lol = a,
    nombres = nombres_campeones, 
    filtro = ['Champion_ban', 'Team_ban', 'Number_ban'],
    drop_level_0 = False)

x.mapa_calor_top_n(
    top_n = top_n_baneo, 
    nombre_campeon = nombres_campeones)

x.grafico_barras_top_n(
    top_n = top_n_baneo, 
    nombres = nombres_campeones,
    titulo = 'Most bans in League of Legends',
    etiqueta_x = 'Champions', 
    etiqueta_y = 'Frequency',
    gama_paleta = 'team', 
    degrade = False,
    etiqueta_barra = False)



y = GraficaGeneralOro()

y.grafico_oro_vs_tiempo(
    b, 
    filtro = ['blueTop','blueADC','redTop','redJungle'])

relacion = y.relacion_filtro(
    b, 
    filtro = ['blueTop','blueADC','redTop','redJungle'], 
    indice = 20)

y.grafico_barra_apilado_oro(relacion)



z = GraficaGeneralMuerte()

z.grafico_puntos(c)

z.grafico_puntos_filtrado(c)

c = c.loc[~c.Player.isin(['','None'])]

nombres_jugador = x.nombres(base_lol = c, lon_nombres = 8, 
                              columna = 'Player')

top_n_muertes = z.top_n(base_lol = c, 
                      nombres = nombres_jugador, 
                      filtro = ['Player'],
                      drop_level_0 = False)

z.grafico_barras_top_n(top_n = top_n_muertes, nombres = nombres_jugador,
                       titulo = 'Most kills in League of Legends',
                       etiqueta_x = 'Player', etiqueta_y = 'Frequency',
                       gama_paleta = 'degrade10', degrade = True,
                       etiqueta_barra = True)

c = c.loc[c.Type_kill == 'Victim']
z.grafico_cajas(
    c, 
    columna_filtro = 'Team_kill', 
    columna_bp = 'Time_kill',
    titulo = 'Tiempos para capitalizar muertes',
    etiqueta_x = 'Ejecución de muerte por parte del equipo',
    etiqueta_y = 'Valores',
    gama_paleta = 'baneo')



w = GraficaGeneralMonstruo()

w.grafico_cajas(
    e, 
    columna_filtro = 'Team_monster', 
    columna_bp = 'Time_monster',
    titulo = 'Tiempos para capitalizar monstruos',
    etiqueta_x = 'Ejecución de monstruo por parte del equipo',
    etiqueta_y = 'Dispersión de ejecución',
    gama_paleta = 'aleatorio10')

w.grafico_barras_frecuencias(
    base_lol = e, 
    columna_filtro = 'Type_monster',
    filtro = None,
    titulo = 'Number times executed a monter in LOL',
    etiqueta_x = 'Monsters', 
    etiqueta_y = 'Frequency')



v = GraficaGeneralEstructura()

f = f.loc[~(pd.isna(f.Lane) | pd.isna(f.Type_structure))]

f['Lane_Type_structure'] = f.Lane + ' ' + f.Type_structure

v.grafico_barras_frecuencias(
    base_lol = f, 
    columna_filtro = 'Lane_Type_structure',
    filtro = None,
    titulo = 'Number times executed a structure in LOL',
    etiqueta_x = 'Structure', 
    etiqueta_y = 'Frequency')

g = AlmacenarImagen()
g.Campeon()
