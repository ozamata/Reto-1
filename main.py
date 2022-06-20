import requests
from bs4 import BeautifulSoup
from tkinter.ttk import Treeview
from tkinter import *



Alto=300
Ancho=700
tipoCambio=[]
url=requests.get('https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx')

class TipoCambio:

    def __init__(self,window):
        self.wind=window
        self.wind.title("Tipo de Cambio Moneda SBS")
        self.wind.geometry(str(Ancho)+'x'+str(Alto))
      
        btnExportar=Button(text='Exportar csv',command=self.exportartipo)
        btnExportar.grid(row=2,column=1, pady=5)
        btnMostrar=Button(text='Mostrar tipo de cambio',command=self.scrappingMostrar)
        btnMostrar.grid(row=2,column=0,pady=5)
        self.trvCambioMoneda=Treeview(height=8,columns=('#1','#2'))
        self.trvCambioMoneda.grid(row=0,column=0,columnspan=3,padx=10,pady=5)
        self.trvCambioMoneda.heading('#0',text='Moneda',anchor=CENTER)
        self.trvCambioMoneda.heading('#1',text='Compra',anchor=CENTER)
        self.trvCambioMoneda.heading('#2',text='Venta',anchor=CENTER)
        # EXPORTAR
    def exportartipo(self):
        strTipoCambioExport=""
        for dictMoneda in tipoCambio:
            for clave,valor in dictMoneda.items():
                strTipoCambioExport+=valor
                if clave!='venta':
                    strTipoCambioExport+=','
                else:
                    strTipoCambioExport+='\n'
        fw=open('tipoCambioMoneda.csv','w')
        fw.write(strTipoCambioExport)
        fw.close()
        # MOSTRAR
    def scrappingMostrar(self):
        if(url.status_code==200):
            html=BeautifulSoup(url.text,'html.parser')
            tabla=html.find_all('table',{'id':'ctl00_cphContent_rgTipoCambio_ctl00'})
            for i in range(7):
                fila=html.find('tr',{'id':'ctl00_cphContent_rgTipoCambio_ctl00__'+str(i)})
                moneda=fila.find('td',{'class':'APLI_fila3'})
                valores=fila.find_all('td',{'class':'APLI_fila2'})
                dictMoneda={
                    'moneda':moneda.get_text(),
                    'compra':valores[0].get_text(),
                    'venta':valores[1].get_text(),
                }
                tipoCambio.append(dictMoneda)
                self.trvCambioMoneda.insert('',END,text=moneda.get_text(),values=[valores[0].get_text(),valores[1].get_text()])
                
        else:
            print("error  "+str(url.status_code))

if __name__=="__main__":
    window=Tk()
    app=TipoCambio(window)
    window.mainloop()