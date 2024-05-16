import  sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import random
from sympy import *


def graficar(f_x, page):

    try:
        x = sp.symbols("x")
        # f_x =x**3-4*x+3
        #sp.E**(-x) -x
        print(f_x)
        x_vals = []
        y_vals = []

        # encontrar dominio de f(x) #
        dominio = sp.calculus.util.continuous_domain(f_x, x, sp.S.Reals)
        print("Dominio: ", dominio)
        print("Limite inferior: ", dominio.start)
        print("Limite superior: ", dominio.end)

        # encontrar raices#
        roots = sp.solve(f_x)
        print("Raices: ", roots)
        #print(type(roots[1]))
        #print(type(1))
        raices_reales=0
        raices_compl=0
        i=0
    
        if len(roots)!=0:
            while i<len(roots):
                try :
                    if isinstance(float(roots[i]),float)==True:
                        raices_reales=raices_reales+1
                        i=i+1
                except:
                    raices_compl=raices_compl+1
                    del roots[i]
                    if len(roots)==0:
                        i=i+1
                    else:
                        print("La ecuación no tiene raices")

        #hola=roots.sorted()
        roots.sort()
        print("Raices ordenadas:",roots)
        
        # general valores de x dentro del dominio #
        """
        oo, oo
        R, oo ][ 
        oo, R ][ 
        """
        if raices_reales>0 or raices_compl>0:
            if raices_reales>0:
                if dominio.start.is_infinite and dominio.end.is_infinite:
                    x_vals = np.linspace(float(roots[0]-10), float(roots[-1]+10), 1000)
                else:
                # si el limite superior/derecha es infinito
                    if dominio.end.is_infinite:

                        if dominio.left_open:
                            x_vals = np.linspace(float(dominio.start)+0.001, float(roots[-1]+10), 1000)

                        else:
                            x_vals = np.linspace(float(dominio.start), float(roots[-1]+10), 1000)

        # si el limite inferior/izquierda es infinito
                    elif dominio.start.is_infinite:
                        if dominio.right_open:
                            x_vals = np.linspace(float(roots[-1]-10), float(dominio.end)-0.001, 1000)

                        else:
                            x_vals = np.linspace(float(roots[-1]-10), float(dominio.end), 1000)

                print("Valores de x: ")
                print(x_vals)

        # Obtener valores de f(x) #
                for x_val in x_vals:
                    y_vals.append(f_x.subs(x, x_val).evalf() )  

                print("Valores de y: ")
                print(y_vals)

        # graficar #
                fig, ax = plt.subplots()
                ax.plot(x_vals, y_vals, label=f"{f_x}", color="green")
                ax.set_title("Método Gráfico")
                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")
                ax.grid("both")
                colors=[]
                for _ in range(len(roots)):
                    color=(random.random(),random.random(),random.random())
                    colors.append(color)
            
                for i in range(len(roots)):
                    ax.scatter(roots[i],roots[i]*0 ,  color=colors[i],label=(float(roots[i])))        
            
        # plt.text(roots, [0] * len(roots), "x=", fontsize=10)
                #page.add(MatplotlibChart(fig, expand=True))
                
                ax.legend()
                plt.show()
            else:
                print("La ecuacion no cuenta con raices reales") 
    except:
        print('error en la funcion')
