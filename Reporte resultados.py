from Organizar_bases import OrganizarBase
from Graficas_generales import (GraficaGeneralBaneo, GraficaGeneralOro,
                                GraficaGeneralMuertes)

x = OrganizarBase()
a,b,c,d,e,f = x.arreglar_base()


x = GraficaGeneralBaneo()
nombres_campeones = x.nombres(base_lol = a, lon_nombres = 6, 
                              columna = 'Champion_ban')
top_n_baneo = x.top_n(base_lol = a, 
                      nombres = nombres_campeones, 
                      filtro = ['Champion_ban'],
                      drop_level_0 = False)

x.mapa_calor_top_n(top_n = top_n_baneo, 
                   nombre_campeon = nombres_campeones) #Corregir cuando
#es un solo filtro
x.grafico_barras_top_n(top_n = top_n_baneo, nombres = nombres_campeones,
                       titulo = 'Most bans in League of Legends',
                       etiqueta_x = 'Champions', etiqueta_y = 'Frequency',
                       gama_paleta = 'degrade10', degrade = True,
                       etiqueta_barra = False)



y = GraficaGeneralOro()
y.grafico_oro_vs_tiempo(b, filtro = ['blueTop','blueADC','redTop','redJungle'])
relacion = y.relacion_filtro(b, filtro = ['blueTop','blueADC','redTop','redJungle'], indice = 20)
y.grafico_barra_apilado_oro(relacion)



z = GraficaGeneralMuertes()
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