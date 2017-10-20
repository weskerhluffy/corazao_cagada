'''
Created on 18/10/2017

@author: 
'''
import logging
import sys
from Queue import Queue


nivel_log = logging.ERROR
#nivel_log = logging.DEBUG
logger_cagada = None

class caca():
    def __init__(self, idx, kk):
        self.idx = idx
        self.kk = kk
        self.tropas = 0
        self.vecinos = None
        self.tropas_comunes = 0
        self.defendible = False
    def __repr__(self):
        return "[[idx {},tropas {}, tropas comunes {}, defendible {}]]".format(self.idx, self.tropas, self.tropas_comunes, self.defendible)
    
    def decrementar_tropas(self, tropas_decrementadas):
        self.tropas_comunes -= tropas_decrementadas
        if(self.tropas_comunes < self.kk):
            self.defendible = False

def korazao_cagada_bfs(nodo_inicial, ya_vistos):
    ya_vistos_inicial = len(ya_vistos)
    
    cacaq = []
    num_tropas = 0
    
    cacaq.append(nodo_inicial)
    ya_vistos.add(nodo_inicial)
    
    while(cacaq):
        nodo_act = cacaq.pop()
        num_tropas += nodo_act.tropas
        logger_cagada.debug("tropas act {} en ciudad {}".format(num_tropas, nodo_act))
        for mierda in nodo_act.vecinos:
            if mierda.defendible and mierda not in ya_vistos:
                cacaq.append(mierda)
                ya_vistos.add(mierda)
    
    ya_vistos_final = len(ya_vistos)
    return ya_vistos_final - ya_vistos_inicial, num_tropas

def korazao_cagada_core(ciudades):
    ya_vistos = set()
    max_tropas = 0
    max_ciudades = 0
    
    for idx, ciudad in enumerate(ciudades):
        if(ciudad not in ya_vistos and ciudad.defendible):
            num_ciudades, num_tropas = korazao_cagada_bfs(ciudad, ya_vistos)
            # TODO: Solo ai un korazao?
            if(max_ciudades < num_ciudades):
                max_tropas = num_tropas
                max_ciudades = num_ciudades
            logger_cagada.debug("para ciudad {}:{} el unm_ciudades {} el d ttrompas {}".format(idx, ciudad, num_ciudades, num_tropas))
    return max_ciudades, max_tropas

def korazao_cagada_calcula_defendibles(ciudades, kk):
    no_defendibles = Queue()
    
    for ciudad in ciudades:
        ciudad.tropas_comunes = ciudad.tropas + sum([vecino.tropas for vecino in ciudad.vecinos])
        if(ciudad.tropas_comunes >= kk):
            ciudad.defendible = True
    ya_descontado = set()
    for ciudad in ciudades:
        if not ciudad.defendible:
            no_defendibles.put(ciudad)
            ya_descontado.add(ciudad)
    
    while not no_defendibles.empty():
        ciudad_act = no_defendibles.get()
        logger_cagada.debug("en no defendible {}".format(ciudad_act))
        for vecino in ciudad_act.vecinos:
            logger_cagada.debug("verga en el vecino {}".format(vecino))
            vecino.decrementar_tropas(ciudad_act.tropas)
            logger_cagada.debug("aora el vecino {}".format(vecino))
            if(not vecino.defendible and vecino not in ya_descontado):
                no_defendibles.put(vecino)
                ya_descontado.add(vecino)
                

def korazao_cagada_main():
    while True:
        linea = sys.stdin.readline()
        num_ciudades, kk = [int(x) for x in linea.strip().split(" ")]
        if(not num_ciudades):
            break
        ciudades = []
        for i in range(num_ciudades):
            ciudades.append(caca(i, kk))
        for i in range(num_ciudades):
            linea = sys.stdin.readline()
            datos = [int(x) for x in linea.strip().split(" ")]
            tropas = datos[0]
            vecinos = [ciudades[x] for x in datos[2:]]
            ciudades[i].vecinos = vecinos
            ciudades[i].tropas = tropas
        logger_cagada.debug("las ciudades kedaron {}".format(ciudades))
        korazao_cagada_calcula_defendibles(ciudades, kk)
        logger_cagada.debug("despues de masajearlas {}".format(ciudades))
        
        ass, fuck = korazao_cagada_core(ciudades)
        logger_cagada.debug("ciudades {} trompas {}".format(ass, fuck))
        print("{} {}".format(ass, fuck))
        
            
            

if __name__ == '__main__':
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=nivel_log, format=FORMAT)
    logger_cagada = logging.getLogger("asa")
    logger_cagada.setLevel(nivel_log)
    korazao_cagada_main()
