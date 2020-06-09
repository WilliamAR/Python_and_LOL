import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import pandas as pd
from re import sub

class GraficaGeneral(object):
    
    def __init__(self):
        
        '''
        Crea la instancia de Gráfica sin ningún tipo de filtro.
        '''
        
        #Paleta inicial
        self._paleta = {'degrade10':
                        ['#FF1B6B', '#EA2E7B', '#D6428C', '#C1559C', 
                         '#AC69AD', '#987CBD', '#8390CE', '#6EA3DE', 
                         '#5AB7EF', '#45CAFF'],
                        'team': 
                            ['#9FCCFA', '#F20909'],
                        'baneo':
                            ['#ff595e', '#ffca3a', '#8ac926', '#1982c4', 
                             '#1982c4'],
                        'aleatorio10':
                            ['#E74C3C', '#8E44AD', '#3498DB', '#16A085',
                             '#28B463', '#B9770E', '#BA4A00', '#909497',
                             '#7F8C8D', '#273746']}
        
    def paleta_invertida(self, color):
        
        '''
        Parámetros:
            color: Objeto tipo cmap de Matplotlib.

        Return:
            Los colores de manera inversa al cmap.
        '''
    
        reversed_color_map = color.reversed()
        return reversed_color_map
    
    def etiqueta(self, columna):
        
        '''
        Lee una tupla de múltiples niveles de columna y lo retorna en un solo 
        string.
        
        Parámetros:
            columna: str, tupla o lista que contenga las columnas del 
            DataFrame.
            
        Return:
            str o lista de columnas en strings legibles. 
        '''
        
        tipo_baneo = []
        for columna_n in columna:
            etiqueta = sub(r'[^a-zA-Z0-9_\s]', r'', str(columna_n))
            tipo_baneo.append(etiqueta)
        
        return tipo_baneo
    
    def nombres(self, base_lol, columna, lon_nombres = 10):
        #Ver a que se debe que debo crear un valor en la variable "columna"
        
        '''
        Lee un DataFrame de LOL y retorna los nombres más frecuentes bajo 
        algún filtro del DataFrame.
        
        Parámetros:
            base_lol: DataFrame que contenga una columna "Champion_ban" 
            con los nombres de los campeones o un DataFrame que contenga
            la columna "Player" y sea posible detectar una frecuencia dentro 
            del DataFrame.
            
            columna: str, Columna que contiene la frecuencia de los nombres o 
            campeones, según sea el caso.
            
            len_nombres: int, Cantidad de nombres que va a retornar la lista 
            del DataFrame, si la longitud de nombres supera al DataFrame, 
            retornar todos los nombres del DataFrame.
            
        Return:
            Lista de los nombres relevantes en la columna "Champion_ban" o
            "Player" según sea el caso. 
        '''
        
        nombres = base_lol.reset_index().\
            rename(columns = {'index': 'Cantidad'}).\
                groupby([columna], as_index = False).Cantidad.count().\
                    sort_values('Cantidad', ascending = False).\
                        reset_index(drop = True)
                    
        if(len(nombres) > lon_nombres):
            nombres = list(nombres.loc[:(lon_nombres-1), columna])
        else:
            nombres = list(nombres.loc[:(len(nombres)-1), columna])
            print('''
                  len_nombres es {}, mientras que la cantidad de nombres
                  disponibles es {}, por lo tanto retornamos {} nombres.
                  '''.format(lon_nombres, len(nombres)))
        
        return nombres
            
    def top_n(self, base_lol, nombres, filtro,
              drop_level_0 = True):
        
        '''
        Lee una DataFrame y lo retorna los nombres más frecuentes bajo el 
        filtro del DataFrame.
        
        Parámetros:
            base_lol: DataFrame que contenga una columna "Champion_ban" 
            con los nombres de los campeones o un DataFrame que contenga
            la columna "Player" y sea posible detectar una frecuencia dentro 
            del DataFrame.
            
            nombre: Lista, contiene los nombres para la busqueda en el 
            DataFrame.
            
            filtro: Lista, con las columnas del DataFrame.
            
            Si se contruye una gráficas para el "baneo" e indicar
            las subidivisiones de las gráficas, siempre debe contener 
            ['Champion_ban'] en primera posición, se pueden adicionar 
            las columnas ['Team_ban', 'Number_ban'].
            
            Si se construye gráficas para algún filtro de "muertes" e indicar
            las subdivisiones de las gráficas, siempre debe contener
            ['Player'] en primera posición, no es recomendable usar otra 
            columna, pero, es posible si se desea imitar algo como las 
            gráficas de "baneo".
            
            drop_level_0: booleano, si el resultado de TopN tiene como filtro 
            varias columnas del DataFrame usado, se genera un DataFrame 
            MultiIndex, por eso, es necesario poder borrar la primera fila de 
            las columnas, ya que contendran las columnas en primera posición
            el valor "Cantidad", por defecto es True.
            
        Return:
            Dataframe con los filtros y nombres del topN para "Champion_ban" o
            "Player", según sea el caso. 
        '''
        
        top_n = base_lol.loc[base_lol[filtro[0]].isin(nombres)].\
            reset_index().rename(columns = {'index': 'Cantidad'}).\
                groupby(filtro, as_index = False).Cantidad.count()
                
        top_n = top_n.set_index(filtro).unstack(filtro[1:]).loc[nombres]
        
        if drop_level_0 == True:
            top_n = top_n.droplevel(level = 0, axis = 1)
        
        return top_n
    
    def grafico_barras_top_n(self, top_n, nombres, 
                             titulo = 'League of Legends',
                             etiqueta_x = 'x',
                             etiqueta_y = 'Frequency',
                             gama_paleta = 'degrade10',
                             degrade = True,
                             etiqueta_barra = True):
        
        '''
        Toma el DataFrame y retorna un gráfico de barras según los filtros
        aplicados a top_n y los campeones o jugadores nombrados.
        
        Parámetros:
            top_n: DataFrame aplicado en la función top_n.
            
            nombres: Lista entregada por la función nombres o una lista
            propia con los nombres de los campeones o jugadores.
            
            titulo: Título al gráfico grafico_barras_top_n, por defecto 
            'League of Legends'.
            
            etiqueta_x: Nombre del eje x, por defecto 'x'.
            
            etiqueta_y: Nombre del eje y, por defecto 'Frequency'.
            
            gama_paleta: str o list, para el caso str son algunas paletas 
            anexadas para utilizar en las gráficas, pero, tener en cuenta que
            algunas paletas no cubren todo el tamaño de las gráficas, si el 
            número barras es superior a la cantidad de colores en la paleta
            se repetira el número de colores para completar todas la columnas, 
            por defecto 'degrade10', las paletas son:
                * team: 2 colores, para un gráfico diferenciado por equipo.
                
                * baneo: 5 colores, para un gráfico diferenciado por baneo o
                asistencias.
                
                * aleatorio10: 10 colores, para un gráfico de 10 barras en cada 
                campeón.
                
                * degrade10: 10 colores, para un gráfico de 10 barras en cada
                campeón.
                
            La lista tiene que ser permitidos entre los colores de Matplotlib y
            contener la cantidad mínima de barras para cada campeón.
            
            degrade: Booleano, si degrade es True, entonces, tomara diferentes
            tonalidades, de lo contrario, solo mostrara un tono para todos los 
            nombres, es recomendable cuando el filtro de topN es de 
            longitud 1, por defecto, True.
            
            etiqueta_barra: Booleanos, si es True, entonces, anexara el valor
            de la frecuencia en cada barra generada, es recomendable cuando el 
            no hay muchas barras, por defecto, True.
            
        Return:
            Gráfico de barras con los nombres de los campeones y los filtros 
            aplicados.
        '''
            
        #AJUSTE DEL MÉTODO
        maximo = top_n.values.max()*1.15
        width = 0.40
        lon_breaks = len(top_n.columns)
        x = np.arange(len(nombres))
        GG = GraficaGeneral()
        tipo = GG.etiqueta(columna = top_n.columns)
        
        def _etiqueta_encima_barra(rectas):

            '''
            Lee las alturas y longitudes de los intervalos y retorna su valor 
            encima de la barra.
            
            Parámetros:
                rectas: Objeto de tipo AxesSubplot que contenga los parámetros
                de las barras en el barplot.
                
            Return:
                Los textos encima de la barra. 
            '''
        
            for recta in rectas:
                height = recta.get_height()
                ax.annotate('{}'.format(height),
                            xy=(recta.get_x() + recta.get_width() / 2, 
                                height),
                            xytext=(0, 1),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize = 8,
                            color = '#333333')
        
        
        fig, ax = plt.subplots()
        
        num_bars = len(top_n.columns)
        num_colores = len(self._paleta[gama_paleta])
        if num_bars < num_colores:
            bar_colors = self._paleta[gama_paleta]
        else:
            bar_colors = self._paleta[gama_paleta]*(num_bars//num_colores + 1)
        
        
        for n, columna in enumerate(top_n.columns):
            
            grafica_baneo = ax.bar(
                x = (x - width) + width/lon_breaks + n*2*width/lon_breaks,
                height= top_n[columna],
                width = 2*width/lon_breaks,
                color = np.where(degrade == True,
                                 bar_colors,
                                 bar_colors[n]),
                label = tipo[n])
        
            if(etiqueta_barra == True):
                _etiqueta_encima_barra(grafica_baneo)
                
        
        ax.set_ylabel(etiqueta_y)
        ax.set_xlabel(etiqueta_x)
        ax.set_title(titulo)
        ax.set_xticks(x)
        ax.set_xticklabels(nombres)
        ax.set_ylim(0, maximo)
        
        if(lon_breaks > 1):
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        plt.setp(ax.get_xticklabels(), 
                 rotation = 45, 
                 ha="right",
                 rotation_mode = "anchor")
        fig.tight_layout()
        plt.show()
    
    def _filtro(self, base_lol, columna_filtro, filtro):
        
        '''
        Entrega la lista de filtros posibles por la unicidad de la columna
        '''
        
        if filtro == None:
            filtro = list(base_lol[columna_filtro].unique())
            
        return filtro
    
    def _base_lol_filtrados(self, base_lol, columna_filtro, columna_bp, filtro):
        
        '''
        Entrega un lista por cada subconulta del filtro
        '''
        
        base_lol_filtrados = []
        for tipo_filtro in filtro:
            base_lol_filtrados.append(
                base_lol.loc[base_lol[columna_filtro] == tipo_filtro, 
                             columna_bp])
            
        return base_lol_filtrados
        
        
    
    def grafico_cajas(self, base_lol, columna_filtro, columna_bp, filtro = None, 
                      titulo = '', etiqueta_x = 'x', etiqueta_y = 'Valores',
                      gama_paleta = 'aleatorio10'):
        
        '''
        Toma el DataFrame y retorna un gráfico de cajas según los filtros
        aplicados a top_n y los campeones o jugadores nombrados.
        
        Parámetros:
            base_lol: DataFrame que contenga una columna numérica para ver
            la dispersión de los puntos dentro del DataFrame.
            
            columna_filtro: str, Columna que se subdividen los grupos.
            
            columna_bp: str, Columna númerica.
            
            filtro: lista o None, Busca las categorías de los filtros dentro 
            de la columnas, si es None, tomará todos los valores únicos del 
            DataFrame.
            
            titulo: Título al gráfico grafico_cajas, por defecto ''.
            
            etiqueta_x: Nombre del eje x, por defecto 'x'.
            
            etiqueta_y: Nombre del eje y, por defecto 'Valores'.
            
            gama_paleta: str o list, para el caso str son algunas paletas 
            anexadas para utilizar en las gráficas, pero, tener en cuenta que
            algunas paletas no cubren todo el tamaño de las gráficas, si el 
            número barras es superior a la cantidad de colores en la paleta
            se repetira el número de colores para completar todas la columnas, 
            por defecto 'degrade10', las paletas son:
                * team: 2 colores, para un gráfico diferenciado por equipo.
                
                * baneo: 5 colores, para un gráfico diferenciado por baneo o
                asistencias.
                
                * aleatorio10: 10 colores, para un gráfico de 10 barras en cada 
                campeón.
                
                * degrade10: 10 colores, para un gráfico de 10 barras en cada
                campeón.
                
            La lista tiene que ser permitidos entre los colores de Matplotlib y
            contener la cantidad mínima de barras para cada campeón.
            
        Return:
            Gráfico de cajas según los filtros especificados.
        '''
        
        GG = GraficaGeneral()
        filtro = GG._filtro(base_lol, columna_filtro, filtro)
        
        base_lol_filtrados = GG._base_lol_filtrados(
            base_lol, columna_filtro, columna_bp, filtro)
        
        fig, ax1 = plt.subplots(figsize=(10, 6))
        fig.canvas.set_window_title('A Boxplot Example')

        bp = ax1.boxplot(base_lol_filtrados, notch=0, vert=1, whis=1.5,
                         labels = filtro)
        plt.setp(bp['boxes'], color='black')
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='white', marker='_')
        
        ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
        
        ax1.set_axisbelow(True)
        ax1.set_title(titulo)
        ax1.set_xlabel(etiqueta_x)
        ax1.set_ylabel(etiqueta_y)
        
        
        num_boxes = len(base_lol_filtrados)
        num_colores = len(self._paleta[gama_paleta])
        if num_boxes < num_colores:
            box_colors = self._paleta[gama_paleta]
        else:
            box_colors = self._paleta[gama_paleta]*(num_boxes//num_colores + 1)
        
        medians = np.empty(num_boxes)
        for i in range(num_boxes):
            box = bp['boxes'][i]
            boxX = []
            boxY = []
            for j in range(5):
                boxX.append(box.get_xdata()[j])
                boxY.append(box.get_ydata()[j])
            box_coords = np.column_stack([boxX, boxY])

            ax1.add_patch(Polygon(box_coords, facecolor=box_colors[i]))

            med = bp['medians'][i]
            medianX = []
            medianY = []
            for j in range(2):
                medianX.append(med.get_xdata()[j])
                medianY.append(med.get_ydata()[j])
                ax1.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]

            ax1.plot(np.average(med.get_xdata()), 
                     np.average(base_lol_filtrados[i]),
                     color='black', marker='s', markeredgecolor='k')
            
        ax1.set_xlim(0.5, num_boxes + 0.5)
        top = base_lol[columna_bp].values.max() + 5
        bottom = 0
        ax1.set_ylim(bottom, top)
        ax1.set_xticklabels(filtro,
                            rotation=45, fontsize=12)
        
        pos = np.arange(num_boxes) + 1
        upper_labels = [str(np.round(s, 2)) for s in medians]
        for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
            ax1.text(pos[tick], .95, upper_labels[tick],
                     transform=ax1.get_xaxis_transform(),
                     horizontalalignment='center', size='x-large', 
                     color=box_colors[tick])
        plt.show()
        
        
    def grafico_barras_frecuencias(self, base_lol, columna_filtro,  
                               filtro = None, titulo = '',
                               etiqueta_x = 'x', etiqueta_y = 'y',
                               gama_paleta = 'degrade10', 
                               etiqueta_barra = True):
        
        '''
        Toma el DataFrame y retorna un gráfico de cajas según los filtros
        aplicados a top_n y los campeones o jugadores nombrados.
        
        Parámetros:
            base_lol: DataFrame que contenga una columna numérica para ver
            las frecuencias dentro del DataFrame.
            
            columna_filtro: str, Columna que se subdividen los grupos.
            
            filtro: lista o None, Busca las categorías de los filtros dentro 
            de la columnas, si es None, tomará todos los valores únicos del 
            DataFrame.
            
            titulo: Título al gráfico grafico_cajas, por defecto ''.
            
            etiqueta_x: Nombre del eje x, por defecto 'x'.
            
            etiqueta_y: Nombre del eje y, por defecto 'Valores'.
            
            gama_paleta: str o list, para el caso str son algunas paletas 
            anexadas para utilizar en las gráficas, pero, tener en cuenta que
            algunas paletas no cubren todo el tamaño de las gráficas, si el 
            número barras es superior a la cantidad de colores en la paleta
            se repetira el número de colores para completar todas la columnas, 
            por defecto 'degrade10', las paletas son:
                * team: 2 colores, para un gráfico diferenciado por equipo.
                
                * baneo: 5 colores, para un gráfico diferenciado por baneo o
                asistencias.
                
                * aleatorio10: 10 colores, para un gráfico de 10 barras en cada 
                campeón.
                
                * degrade10: 10 colores, para un gráfico de 10 barras en cada
                campeón.
                
            La lista tiene que ser permitidos entre los colores de Matplotlib y
            contener la cantidad mínima de barras para cada campeón.
            
        Return:
            Gráfico de barras según los filtros especificados.
        '''
        
        GG = GraficaGeneral()
        filtro = GG._filtro(base_lol, columna_filtro, filtro)
        
        base_lol_filtrados = GG._base_lol_filtrados(
            base_lol, columna_filtro, columna_filtro, filtro)
        
        #AJUSTE DEL MÉTODO
        width = 0.40
        x = np.arange(len(filtro))
        num_bars = len(base_lol_filtrados)
        colores = self._paleta[gama_paleta]
        num_colores = len(colores)
        if num_bars < num_colores:
            bar_colors = colores
        else:
            bar_colors = colores*(num_bars//num_colores + 1)
            
        frec_monstruo = []
        for tipo in base_lol_filtrados:
            frec_monstruo.append(len(tipo))
        maximo = max(frec_monstruo)*1.15
        
        def _etiqueta_encima_barra(rectas):

            '''
            Lee las alturas y longitudes de los intervalos y retorna su valor 
            encima de la barra.
            
            Parámetros:
                rectas: Objeto de tipo AxesSubplot que contenga los parámetros
                de las barras en el barplot.
                
            Return:
                Los textos encima de la barra. 
            '''
        
            for recta in rectas:
                height = recta.get_height()
                ax.annotate('{}'.format(round(height,2)),
                            xy=(recta.get_x() + recta.get_width() / 2, 
                                height),
                            xytext=(0, 1),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize = 8,
                            color = '#333333')
        
        fig, ax = plt.subplots() 
        grafica = ax.bar(x = x, height = frec_monstruo, width = width, 
                color = bar_colors[:num_bars])
        
        if(etiqueta_barra):
            _etiqueta_encima_barra(grafica)
                    
        ax.set_ylabel(etiqueta_y)
        ax.set_ylim(0, maximo)
        ax.set_xlabel(etiqueta_x)
        ax.set_title(titulo)
        ax.set_xticks(x)
        ax.set_xticklabels(filtro)
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
        plt.setp(ax.get_xticklabels(), 
                 rotation = 45, 
                 ha="right",
                 rotation_mode = "anchor")
        fig.tight_layout()
        plt.show()
    
        

class GraficaGeneralBaneo(GraficaGeneral):
    
    def __init__(self):
        
        '''
        Crea la instancia de Gráfica para la base de datos que contiene 
        el baneo de los campeones antes de comenzar la partida.
        '''
        super().__init__()
    
    def mapa_calor_top_n(self, top_n, nombre_campeon, color_invertido = True):
        
        '''
        Toma el DataFrame y retorna un gráfico de calor según los filtros
        aplicados a top_n y los campeones nombrados.
        
        Parámetros:
            top_n: DataFrame aplicado en la función top_n.
            
            nombre_campeon: Lista entregada por la función nombres o una lista
            propia con los nombres de los campeones.
            
            color_invertido: El color para el mapa_calor_top_n es 'hot', y 
            se inicia con un color oscuro hasta un color claro, pero, si
            color_invertido es True, entonces cambia la escala, de tal manera 
            en que inicia en un color claro hasta un color oscuro, por 
            defecto es True.
            
        Return:
            Mapa de calor con los nombres y los filtros aplicados.
        '''
        
        cantidad = top_n.values
        GGB = GraficaGeneralBaneo()
        tipo_baneo = GGB.etiqueta(columna = top_n.columns)
        cuantil = np.quantile(cantidad, 0.75)
        
        if(len(nombre_campeon) > 10):
            tamaño_numero = 7
        else:
            tamaño_numero = 10
        
        paleta = 'hot'
        color_mapa = plt.cm.get_cmap(paleta)
        if color_invertido:
            color_mapa = GGB.paleta_invertida(color_mapa)
            color_matriz = np.where(cantidad < cuantil, 'black', 'white') 
        else:
            color_matriz = np.where(cantidad < cuantil, 'white', 'black')
        
        fig, ax = plt.subplots()
        im = ax.imshow(cantidad, cmap = color_mapa)
        

        ax.set_xticks(np.arange(len(tipo_baneo)))
        ax.set_yticks(np.arange(len(nombre_campeon)))

        ax.set_xticklabels(tipo_baneo)
        ax.set_yticklabels(nombre_campeon)
        
        plt.setp(ax.get_xticklabels(), rotation=45, 
                 ha="right", rotation_mode="anchor")

        for i in range(len(nombre_campeon)):
            for j in range(len(tipo_baneo)):
                ax.text(j, i, cantidad[i, j], ha="center", 
                        va="center", color = color_matriz[i,j],
                        fontsize = tamaño_numero)
        
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Frequency', rotation=-90, va="bottom")
        
        ax.set_xticks(np.arange(cantidad.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(cantidad.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=2)
        ax.tick_params(which="minor", bottom=False, left=False)
        
        
        ax.set_title('Most bans in League of Legends')
        fig.tight_layout()
        plt.show()

class GraficaGeneralOro(GraficaGeneral):
    
    def __init__(self):
        
        '''
        Crea la instancia de Gráfica para la base de datos que contiene 
        el crecimiento de oro durante las partidas.
        '''
        super().__init__()
    
    def etiqueta_oro(self, columnas, tipo):
        
        '''
        Lee las columnas de un DataFrame y selecciona un filtro según el 
        tipo.
        La columna Time_gold debe ser incluida
        
        Parámetros:
            columnas: Columnas de un DataFrame que contengan la columna
            "Time_gold".
            
            tipo: str, realiza un filtro para las columnas que contengan
            el tipo.
            
        Return:
            Las columnas que validen el filtro. 
        '''
        
        return columnas[columnas.str.contains(tipo + '|Time_gold')]
        
    def grafico_oro_vs_tiempo(self, oro, filtro = None, indice = 10):
        
        '''
        Toma el DataFrame y realiza un gráfico según la serie de tiempo.
        
        Parámetros:
            oro: DataFrame, debe contener la columna 'Time_gold' y en lo
            posible las columnas sean numéricas.
            
            filtro: None o lista, Indica la separacion de columnas, según
            el filtro realizado, por defecto es None, es decir todas las 
            columnas se calculan de manera individual.
            
            indice: Opcional, escalar. Si el gráfico realiza dos lineas,
            se puede incluir la diferencia monetaria, por defecto es 10.
            
        Return:
            Gráfico lineal en relación al crecimiento del dinero durante la
            partida. 
        
        '''
        
        GGO = GraficaGeneralOro()
        columnas = oro.columns
        
        if(filtro == None):
            filtro = GGO.etiqueta_oro(columnas, tipo = '[^Address]')
        
        
        def etiqueta_diferencia_oro(diferencia, indice = 10):
            
            '''
            Toma el DataFrame y entrega las etiquetas según la diferencia
            del DataFrame.
            
            Parámetros:
                diferencia: DataFrame, columnas numéricas.
                
                indice: escalar. Si el gráfico realiza dos lineas,
                se puede incluir la diferencia monetaria, por defecto es 10.
                
            Return:
                Gráfico lineal en relación al crecimiento del dinero durante la
                partida.
            '''
        
        
            for i, texto in zip(
                    diferencia.loc[(diferencia.index %indice == 0) |
                                   (diferencia.index == 1)].index,
                    diferencia.loc[(diferencia.index %indice == 0) |
                                   (diferencia.index == 1)].round().astype(int)):
                
                ax.text(i, 10, texto, ha="center", va="center", 
                        color = '#F20909', fontsize = 10)
        
        
        
        fig, ax = plt.subplots()
        for tipo in filtro:
            if(tipo == 'Time_gold'):
                continue
            
            cantidad = oro.loc[:,GGO.etiqueta_oro(columnas, tipo)].\
                groupby('Time_gold').mean().apply(np.sum, axis = 1)
            
            ax.plot(cantidad.index, cantidad.values, 
                     alpha = 0.8, label = tipo)        
        
        if len(filtro) == 2:
            diferencia = GGO.diferencia_oro(oro, filtro, columnas)
            etiqueta_diferencia_oro(diferencia, indice)
        
        ax.set_xticks(cantidad.loc[(cantidad.index %indice == 0) |
                                   (cantidad.index == 1)].index)
        ax.set_yticklabels(np.array((ax.get_yticks()/1000), dtype = 'int'))
        ax.set_ylabel('Gold in K')
        ax.set_xlabel('Time')
        ax.set_title('Gold average in League of Legends')
        ax.legend()
        plt.show()
        
        
    def diferencia_oro(self, oro, filtro, columnas):
        
        '''
        Toma el DataFrame y entrega las etiquetas según la diferencia
        del DataFrame.
        
        Parámetros:
            oro: DataFrame, debe contener la columna 'Time_gold' y en lo
            posible las columnas sean numéricas.
            
            filtro: None o lista, Indica la separacion de columnas, según
            el filtro realizado, es decir, bajo que criterio desea en que
            se vea la diferencia, por equipo?, por posición?, 
            por defecto es None, es decir, todas las columnas se calculan 
            de manera individual.
            
            columnas: Columnas de un DataFrame.
            
        Return:
            Retorna la diferencia entre columnas organizadas, la primera
            columna suma y el resto de columnas restan el valor de la 
            inicial.
        '''
        
        GGO = GraficaGeneralOro()
        
        if(filtro == None):
            filtro = GGO.etiqueta_oro(columnas, tipo = '[^Address]')
        
        diferencia = 0
        for i,tipo in enumerate(filtro):
            if(i == 0):
                diferencia += oro.loc[:,GGO.etiqueta_oro(columnas, tipo)].\
                        groupby('Time_gold').mean().apply(np.sum, axis = 1)
            else:
                diferencia -= oro.loc[:,GGO.etiqueta_oro(columnas, tipo)].\
                        groupby('Time_gold').mean().apply(np.sum, axis = 1)
        
        return diferencia
    
    def relacion_filtro(self, oro, filtro, indice = 10):
        
        '''
        Parámetros:
            oro: DataFrame, columnas numéricas, debe contener la columna
            Time_gold.
                
            filtro: None o lista, Indica la separacion de columnas, según 
            el filtro realizado, es decir, bajo que criterio desea en que 
            se vea la diferencia, por equipo?, por posición?, por defecto es 
            None, es decir, todas las columnas se calculan de manera 
            individual.
            
            indice: escalar. Ver en intervalos el crecimiento del oro durante 
            el tiempo.
                
        Return:
            Retorna un DataFrame con la relación de las columnas según el 
            filtro durante el tiempo.
        '''
        
        GGO = GraficaGeneralOro()
        
        relacion = pd.DataFrame()
        for tipo in filtro:
            if(tipo == 'Time_gold'):
                continue
            relacion_tipo = oro.loc[:,GGO.etiqueta_oro(oro.columns, tipo)].\
                groupby('Time_gold').mean().apply(np.sum, axis = 1)
                
            relacion = pd.concat([relacion, relacion_tipo], axis = 1)
        
        if(type(filtro) == list):
            relacion.columns = filtro
        else:
            try:
                relacion.columns = filtro.drop('Time_gold')
            except KeyError:
                relacion.columns = filtro
        
        relacion.index = oro.Time_gold.unique()
        relacion = relacion.loc[(relacion.index % indice == 0) |
                                (relacion.index == 1)]
        
        return relacion

    
    def grafico_barra_apilado_oro(self, relacion):
        
        '''
        Parámetros:
            relacion: DataFrame, contiene la relación de las columnas,
            según el filtrado especificado.
                
        Return:
            Gráfico de barras apilado por la cantidad columnas que existan 
            durante el tiempo en intervalos dados por la relación.
        '''
        
        
        relacion.plot(kind='bar', stacked=True)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.grid(True, color="gray", linestyle='-', linewidth=2, alpha = 0.2)
        plt.title('Gold in League of Legends')
        plt.xlabel('Time')
        plt.ylabel('Gold')
        plt.show()

class GraficaGeneralMuerte(GraficaGeneral):
    
    def __init__(self):
        
        '''
        Crea la instancia de Gráfica para la base de datos que contiene 
        eliminación de personajes.
        '''
        super().__init__()
        
        
    def grafico_puntos(self, muertes, paleta = 'magma', filtro = None,
                       color_invertido = True, tiempo_ordenado = True, a = 0.5):
        
        '''
        Parámetros:
            muertes: DataFrame, contiene las muertes realizadas en el juego.
            
            paleta: str, paleta de colores permitidos en Matplotlib.
            
            filtro: Si no contiene un filtro, supondrá que no hay más puntos
            en la lista, es decir, el gráfico no viene de la función 
            grafico_puntos_filtrado, por defecto None.
            
            color_invertido: El color para el mapa_calor_top_n es 'magma', y 
            se inicia con un color oscuro hasta un color claro, pero, si
            color_invertido es True, entonces cambia la escala, de tal manera 
            en que inicia en un color claro hasta un color oscuro, por 
            defecto es True.
            
            tiempo_ordenado: boolean, organiza las muertes según el tiempo
            de manera ascendente.
            
            a: Según la cantidad de filtros realizados se puede sobreponer los
            puntos y hacer que se vea una sola tonalidad, entonces a, 
            corresponde al alpha de las gráficas de Matplotlib y entre más 
            cercanos a 0 se puede ver mejor los puntos que se ubican detras de
            otros puntos, por defecto es 0.5.
                
        Return:
            Gráfico de puntos para la ubicación de las muertes durante la
            partida.
        '''
        GGM = GraficaGeneralMuerte()
        muertes = muertes.drop_duplicates(['Address', 'x_pos', 'y_pos'])
            
        if tiempo_ordenado == True:
            muertes = muertes.sort_values('Time_kill').reset_index(drop = True)
        
        
        color_map = plt.cm.get_cmap(paleta)
        if color_invertido == True:
            color_map = GGM.paleta_invertida(color_map)
        
        figure = plt.figure
        ax = plt.gca()
        im = ax.scatter(x = muertes.x_pos, y = muertes.y_pos, 
                        c = muertes.Time_kill, cmap = color_map, 
                        alpha = a, s = 0.1)
        
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Frequency', rotation=-90, va="bottom")
        
        if filtro == None:
            ax.set_xlabel('Position X')
            ax.set_ylabel('Position Y')
            ax.set_title('Kills in League of Legends')
            plt.show()
    
    
    def grafico_puntos_filtrado(self, muertes, 
                                paleta = ['Reds','Blues'], 
                                columna = 'Team_kill',
                                color_invertido = True, 
                                tiempo_ordenado = True,
                                a = 0.07):
        
        '''
        Parámetros:
            muertes: DataFrame, contiene las muertes realizadas en el juego.
            
            paleta: str o lista, paleta de cmap permitidos en Matplotlib,
            debe contener la misma cantidad de cmap, por la cantidad de 
            grupos que aparezca en en la variable 'columna'.
            
            columna: str, Contiene la columna a la cual se desea agrupar y 
            diferenciar las muertes, por defecto, 'Team_kill', si no tiene
            algún filtro, remitase a la función 'grafico_puntos'.
            
            color_invertido: El color para el mapa_calor_top_n es 'magma', y 
            se inicia con un color oscuro hasta un color claro, pero, si
            color_invertido es True, entonces cambia la escala, de tal manera 
            en que inicia en un color claro hasta un color oscuro, por 
            defecto es True.
            
            tiempo_ordenado: boolean, organiza las muertes según el tiempo
            de manera ascendente.
            
            a: Según la cantidad de filtros realizados se puede sobreponer los
            puntos y hacer que se vea una sola tonalidad, entonces a, 
            corresponde al alpha de las gráficas de Matplotlib y entre más 
            cercanos a 0 se puede ver mejor los puntos que se ubican detras de
            otros puntos, por defecto es 0.07.
                
        Return:
            Gráfico de puntos para la ubicación de las muertes durante la
            partida.
        '''
        
        GGM = GraficaGeneralMuerte()
        
        if columna == None:
            GGM.grafico_puntos(muertes = muertes, 
                               paleta = paleta, 
                               filtro = None, 
                               color_invertido = color_invertido, 
                               tiempo_ordenado = tiempo_ordenado)
        else:
            filtro = muertes[columna].unique()
            for n, tipo in enumerate(filtro):
                sub_m = muertes.loc[muertes[columna].isin([tipo])]
                grafico = GGM.grafico_puntos(muertes = sub_m, 
                                   paleta = paleta[n], 
                                   filtro = tipo, 
                                   color_invertido = color_invertido, 
                                   tiempo_ordenado = tiempo_ordenado,
                                   a = a)
                
            plt.show()

class GraficaGeneralMonstruo(GraficaGeneral):
    
    def __init__(self):
        
        '''
        Crea la instancia de Gráfica para la base de datos que contiene 
        eliminación de monstruos.
        '''
        super().__init__()

        
class GraficaGeneralEstructura(GraficaGeneral):
    
    def __init__(self):
        
        '''
        Crea la instancia de Gráfica para la base de datos que contiene 
        eliminación de monstruos.
        '''
        super().__init__()
        