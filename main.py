import sympy as sp
from sympy import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

import flet as ft

# from metodos.biseccion import biseccion
# from metodos.graficador import graficar

def biseccion(txt_x1, txt_xu, txt_fx, txt_cifras_sig, lbl_resultados, resultados, page):
    
    def eval_infx(xn, fx):
        return fx.subs(x, xn)
    
    def tolerancia(cifras_sig):
        Es = 0.5 * 10 ** (2 - cifras_sig)
        return Es
    
    def headers(df : pd.DataFrame) -> list:
        return [ft.DataColumn(ft.Text(header)) for header in df.columns]

#    Función para generar las filas de la DataTable
    def rows(df : pd.DataFrame) -> list:
        rows = []
        for index, row in df.iterrows():
            rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(str(row[header]))) for header in df.columns]))
        return rows
    
    x = sp.symbols('x')
    
    x1 = float(txt_x1.value)
    xu = float(txt_xu.value)
    fx = sp.sympify(txt_fx.value)
    cifras_sig = float(txt_cifras_sig.value)

    
    Es = tolerancia(cifras_sig)
    
    iteracion = 1
    aprox_anterior = 0
    aprox_actual = 0
    # def f(x):
    #     return (( e**-x)-x) 
    df = pd.DataFrame(columns=["Iteracion", "x1", "xu", "xr", "f(x1)", "f(xu)", "f(xr)", "f(x1)*f(xr)", "Condicion", "Error Aproximado"])

    #print('Intervalo [', x1,',',xu,']')

    while True:

        xr = (x1 + xu)/ 2
        fx1 = eval_infx(x1, fx)
        fxu = eval_infx(xu, fx)
        fxr = eval_infx(xr, fx)
        producto = fx1*fxr

        if producto < 0:
            condicon = '< 0'
        else:
            condicon = '> 0'
        Ea = abs(((xr - aprox_anterior)/xr)*100)
        df.loc[iteracion-1] = [iteracion, x1, xu, xr, fx1, fxu, fxr, producto, condicon,  Ea]
    
        if producto < 0:
            xu = xr
        elif producto > 0:
            x1 = xr
        else:
            break
        if Ea < Es:
            break
        
        aprox_anterior = xr
        iteracion += 1 
    
    lbl_resultados.value = f"La Raiz es: {xr} \nCon un error de: {Ea}% \nCon {iteracion} iteraciones"
    resultados.visible = True
    # grafico.graficar(fx, page)
    
    tbl_dataTable = ft.DataTable(
        columns=headers(df),
        rows=rows(df)
    )
    
    
    tbl = ft.Row(
            [
                ft.Container(
                    #width=500,
                    #bgcolor='#565656',  #ft.colors.BLUE_100,
                    border_radius=ft.border_radius.all(20),
                    padding=20,
                    content=ft.Row(
                        [
                        tbl_dataTable
                        ]
                        
                    ),
                )   
            ], 
            scroll=ft.ScrollMode.ALWAYS #Permite el scroll
        
    )
    
    listview = ft.ListView(expand=1, auto_scroll=True )
    listview.controls.append(tbl)
    page.add(listview)
    
    
    page.update()
 
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
   

def main(page: ft.page):
    
    def calcular(event):
        state_x1 = txt_x1.value
        state_xu = txt_xu.value
        state_fx = txt_fx.value
        state_cifras = txt_cifras_sig.value
        
        if state_x1 == '' or state_xu == '' or state_cifras == '' or state_fx == '':
            print('VACIO')
            show_alert(event)
        else:
            biseccion(txt_x1, txt_xu, txt_fx, txt_cifras_sig, lbl_resultados, resultados, page)
            # fx = sp.sympify(txt_fx.value)
            # graficar(fx, page)
  
    def grafica(event):
        
        state_x1 = txt_x1.value
        state_xu = txt_xu.value
        state_fx = txt_fx.value
        state_cifras = txt_cifras_sig.value
        
        if state_x1 == '' and state_xu == '' and state_cifras == '' and state_fx == '':
            show_alert(event)
        else:
            try:
                if validar_expresion(txt_fx.value):
                    
                    fx = sp.sympify(txt_fx.value)
                    graficar(fx, page)
                else:
                    show_alert(event)
                
            except:
                show_alert(event)
    
    def validar_expresion(expresion):
        # Lista de operadores matemáticos válidos y caracteres permitidos en los símbolos
        caracteres_permitidos = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._+-*/^() ')
        operadores_permitidos = set('+-*/^')

        # Verificar si la expresión contiene al menos un símbolo o un operador matemático válido
        if any(caracter in caracteres_permitidos for caracter in expresion) and \
        any(op in operadores_permitidos for op in expresion):
            try:
                # Intenta convertir la expresión en una expresión SymPy
                sp.sympify(expresion)
                return True  # La expresión es válida
            except (sp.SympifyError, TypeError):
                pass

        return False  # La expresión no es válida   
        
    def close_alert(event):
        # event.control.page.banner.open = False\
        page.banner.open = False
        page.update()
       
    def show_alert(event):
        # event.control.page.banner = banner
        # event.control.page.banner.open = True
        # page.update()
        page.banner = banner
        page.banner.open = True
        page.update()
        
    def limpiar (event):
        txt_x1.value = ''
        txt_xu.value =''
        txt_fx.value = ''
        txt_cifras_sig.value = ''
        txt_x1.autofocus=True
        resultados.visible=False
        page.update()        
    
    txt_x1 = ft.TextField(label='Ingrese valor x1')
    txt_xu = ft.TextField(label='Ingrese valor xu')
    txt_cifras_sig = ft.TextField(label='Cifras')
    txt_fx = ft.TextField(label='Ingrese funcion')
    btn_calcular = ft.ElevatedButton(text='Calcular', on_click=calcular)
    lbl_resultados = ft.Text()
    btn_limpiar = ft.ElevatedButton(text='Limpiar', on_click=limpiar)
    btn_graficar = ft.ElevatedButton(text='Graficar')
    
    resultados = ft.Container(
                    visible=False,
                    bgcolor='#565656',  #ft.colors.BLUE_100,
                    border_radius=ft.border_radius.all(20),
                    padding=20,
                    content=ft.ResponsiveRow(
                        [
                        ft.Container(
                            lbl_resultados,
                            col={"sm": 6, "md": 4, "xl": 12},
                        )
                    ]
                )
            
    )

    banner = ft.Banner(
        bgcolor='#565656',
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=ft.Text(
            "Por favor ingrese valores para calcular"
        ),
        actions=[
            ft.TextButton("Ok", on_click=close_alert),
            
        ],
    )
       
    

    page.add(
        

        ft.Container(
            bgcolor='#565656',  #ft.colors.BLUE_100,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.ResponsiveRow( # Responsive Row me permite dar responsividad a los componentes
                                  
                [
                    ft.Container(
                        txt_x1,
                        col={"sm": 6, "md": 6, "xl": 3}, #la fila se divide en 12 
                    ),
                    ft.Container(
                        txt_xu,
                        col={"sm": 6, "md": 6, "xl": 3},
                    ),
                    ft.Container(
                        txt_cifras_sig,
                        col={"sm": 6, "md": 6, "xl": 3},
                    ),
                    ft.Container(
                        txt_fx,
                        col={"sm": 6, "md": 6, "xl": 3},
                    ),
                    ft.Container(
                        btn_calcular,
                        btn_limpiar,
                        col={"sm": 2, "md": 2, "xl": 2},
                    ),
                    ft.Container(
                        btn_limpiar,
                        col={"sm": 2, "md": 2, "xl": 2},
                    ),
                    ft.Container(
                        btn_graficar,
                        col={"sm": 2, "md": 2, "xl": 2},
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER,   
                        
            ),
                    
        ),
        resultados,
        
        
    )

ft.app(target=main, view=ft.WEB_BROWSER)