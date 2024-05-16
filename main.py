import sympy as sp
from sympy import *

import flet as ft

from biseccion import biseccion
from graficador import graficar


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
