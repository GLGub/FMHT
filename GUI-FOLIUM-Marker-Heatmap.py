import folium as fl
from folium.plugins import HeatMap
import pandas as pd
from tkinter import *
from tkinter import filedialog
from folium.plugins import Geocoder
from folium.plugins import Draw


map_obj = fl.Map(location = [14.602958417652694, 120.97421032461357], zoom_start=5)



def mapgen(center,slideval,mapnameLabel):
    
    cent=list((center.split(',')))
    
    map_obj.location = [cent[0],cent[1]]  # Update the location of the map
    map_obj.center = [cent[0],cent[1]]# Update the center of the map
    map_obj.zoom_start=slideval
    
    Draw(export=False,).add_to(map_obj)
    fl.TileLayer('CartoDB Dark_Matter').add_to(map_obj)
    Geocoder().add_to(map_obj)
    
    fl.LayerControl(position='bottomright').add_to(map_obj)
    
    map_obj.save(f"{mapnameLabel}.html")
    popup(mapnameLabel)


def popup(name):
    statwin=Tk()
    statwin.title("Map Generated")
    statwin.geometry('250x50')

    statwin.eval('tk::PlaceWindow . center')
    stawin1=Label(statwin,text=f"{name} Generated").pack( side = BOTTOM ,pady=10)


def heats(df,color,text,obj):
    global map_obj
    
    #legnds
    df2=pd.read_csv (df)
    lgd_txt = '<span style="color: {col};">{txt}</span>'
    fgsubs=fl.FeatureGroup(name= lgd_txt.format(  txt= obj.upper()+'||'+text+'||'+ color , col= color))
    #heatmaps
    gradient = {
    0.0: color,
    0.5: color,
    1.0: color
    }
    HeatMap(df2,gradient=gradient, radius=10,blur=1).add_to(fgsubs)
    fgsubs.add_to(map_obj)

def marking(df,color,text,obj):
    global map_obj
    df3=pd.read_csv (df)
    lgd_txt = '<span style="color: {col};">{txt}</span>'
    fgmarks=fl.FeatureGroup(name= lgd_txt.format( txt= obj.upper()+'--'+text+'--'+ color, col= color))
    
    for index,row in df3.iterrows():
        iframe = fl.IFrame('Remarks:' + str(row["site"]))
        popup = fl.Popup(iframe, min_width=200, max_width=100)
        fl.Marker(location=[row['long'],row['lat']], 
              popup = popup, icon=fl.Icon(color=color, icon='tower-cell', prefix='fa')).add_to(fgmarks)
        
    fgmarks.add_to(map_obj)


def addtomap(obj,kulay,filtname):
    subscsv=filedialog.askopenfilename()
    if obj == 'HeatMap':
        heats(subscsv,kulay,filtname,obj)
    else:
        marking(subscsv,kulay,filtname,obj)
    textbox_update(kulay,filtname,obj)

def textbox_update(a,b,c):
    mappupdate.config(state="normal")
    mappupdate.insert('end',c+':'+a+': '+b+'\n')
    mappupdate.config(state="disabled")

def addmapwin():
    addmapwin1= Toplevel()
    addmapwin1.title("Add to map")
    addmapwin1.geometry('300x200')
    addmapwin1.resizable(False,False)

    labelwin1=Label(addmapwin1,text='Type').grid(row=0,column=0,sticky='w',ipadx=10)
    
    func1= ['HeatMap','Marker']
    clicked1 = StringVar()
    clicked1.set( "HeatMap" )
    statdrop=OptionMenu(addmapwin1,clicked1 ,*func1)
    statdrop.config(width=10)
    statdrop.grid(row=0,column=1)
    
    labelwin2=Label(addmapwin1,text='Color').grid(row=2,column=0,sticky='w',ipadx=10)
    chose= ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
    'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    colour = StringVar()
    colour.set( "red" )
    #color entry
    statdrop=OptionMenu(addmapwin1,colour ,*chose)
    statdrop.config(width=10)
    statdrop.grid(row=2,column=1) 
    #Filter name
    labelwin3=Label(addmapwin1,text='Filter Name').grid(row=3,column=0,sticky='w',ipadx=10)
    entryfilter= Entry(addmapwin1,width=30)
    entryfilter.grid(row=3,column=1)
    
    addobj=Button(addmapwin1,text="Add to Map",command=lambda: addtomap(clicked1.get(),
                                                                        colour.get(),
                                                                        entryfilter.get()
                                                                        )).grid(row=4,column=0,columnspan=3)
    
    addmapwin1.mainloop()



#Main Window

windowmain= Tk()
windowmain.title("Geo Visual")
windowmain.geometry('400x250')
windowmain.resizable(False,False)

mapnameLabel=Label(windowmain,text='Map Name ').grid(row=0,column=0,sticky='w',ipadx=10)
mapnameLabel= Entry(windowmain,width=40)
mapnameLabel.grid(row=0,column=1)

centerLabel=Label(windowmain,text='').grid(row=1,column=3,sticky='w',ipadx=10)
centerLabel=Label(windowmain,text='Map Center ').grid(row=1,column=0,sticky='w',ipadx=10)
center= Entry(windowmain,width=40)
center.grid(row=1,column=1)

zoomLabel=Label(windowmain,text='Map Zoom level ').grid(row=2,column=0,sticky='w',ipadx=10)
#Slider
slideval=IntVar()
slider = Scale(windowmain,from_=5,to=18,orient='horizontal',variable=slideval,length=200)
slider.grid(row=2,column=1,sticky='w',ipadx=10)

addmapwinbut=Button(windowmain,text="Add Obj to Map",command=addmapwin).grid(row=3,column=0)
mappupdate=Text(windowmain,height=5,width=10)
mappupdate.grid(row=3,column=1,sticky='we',columnspan=3,padx=10,pady=10)



addmapwinbut=Button(windowmain,text="Generate the Map",command=lambda : mapgen(center.get(),
                                                                               slideval.get(),
                                                                               mapnameLabel.get()
                                                                               ),width=40,height=3).grid(row=4,column=0,columnspan=2)



windowmain.mainloop()