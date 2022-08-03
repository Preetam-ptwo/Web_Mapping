from pydoc import html
import folium
import pandas as pd
from folium.plugins import HeatMap
import branca

data=pd.read_csv("data\complete_dataset.csv")

#for popup html decorations
html="""<h4>Population: </h4>%s 
        <br>
        <h4>Average_Income: </h4>%s"""

#for marker color based on avg salary
def color(l):
    if l<17000:
        return 'red'
    elif l<34000:
        return 'orange'
    elif l<51000:
        return 'blue'
    else:
        return 'green'


#creating folium map variable
map = folium.Map(location=[12.983668, 77.588324], zoom_start=12)

#Feature group for Average salary
fgs = folium.FeatureGroup(name="Average Salary(bangalore)")
for i,j,k,l,m in zip(data["Latitude"] , data["Longitude"],data["Population"],data["AverageIncome"],data["Neighborhoods"]):
    iframe=folium.IFrame(html=html % (k,l),width=125, height=125)
    fgs.add_child(folium.Marker(location=[i,j],popup=folium.Popup(iframe),tooltip=m,icon=folium.Icon(color=color(l))))

#Feature group for HeatMap
d=data.iloc[:,3:5]
fgh = folium.FeatureGroup(name="Heat Map(income)",show=False)
fgh.add_child(HeatMap(d,radius=30))

#feature Group for json Population
fgp = folium.FeatureGroup(name="Population(world)")
fgp.add_child(folium.GeoJson(data=open('data\world.json','r',encoding='utf-8-sig').read(),
style_function=lambda x:{'fillColor':'green'if x['properties']['POP2005']<10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

#Adding FeatureGroup for map variable
map.add_child(fgs)
map.add_child(fgp)
map.add_child(fgh)

#Adding Layer Control to map variable
map.add_child(folium.LayerControl())

#Saving map to HTMl file
map.save("map.html")