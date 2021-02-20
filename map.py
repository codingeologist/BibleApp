import folium
import numpy as np
import pandas as pd
import geopandas as gpd
from folium import plugins
from folium.plugins import HeatMap
from MAPBOX_API import MAPBOX_API

def get_data():
    df = pd.read_csv('./Data/mergedplaces_openbibleinfo.csv')
    df['Lat'] = df['Lat'].str.replace(r'>', '')
    df['Lat'] = df['Lat'].str.replace(r'<', '')
    df['Lat'] = df['Lat'].str.replace(r'?', '')
    df['Lat'] = df['Lat'].str.replace(r'~', '')
    
    df['Lon'] = df['Lon'].str.replace(r'>', '')
    df['Lon'] = df['Lon'].str.replace(r'<', '')
    df['Lon'] = df['Lon'].str.replace(r'?', '')
    df['Lon'] = df['Lon'].str.replace(r'~', '')
    
    df = df.replace(r'', np.nan, regex=True)
    df = df.dropna(subset=['Lat', 'Lon'])
    df['Lat'] = df['Lat'].astype(float)
    df['Lon'] = df['Lon'].astype(float)
    
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Lon, df.Lat))
    gdf = gdf.set_crs(epsg=4326, inplace=True)
    return gdf

def make_map(gdf):
    m = folium.Map(location=[gdf.iloc[1]['Lat'], gdf.iloc[1]['Lon']],tiles=MAPBOX_API, attr = 'Mapbox', zoom_start=6)
    
    #points = folium.features.GeoJson(gdf)
    
    for i in range(len(gdf)):
        X = gdf.iloc[i]['Lat']
        Y = gdf.iloc[i]['Lon']
        if str(gdf.iloc[i]['Root']) == np.nan:
               verse = str(gdf.iloc[i]['#ESV'])+'\n'+str(gdf.iloc[i]['Root'])
        else:
            verse = str(gdf.iloc[i]['#ESV'])
            
        folium.CircleMarker([X, Y], radius=2, weight=4, popup=folium.Popup(verse)).add_to(m)
        
    heatmap_data = [[row['Lat'], row['Lon']] for index, row in gdf.iterrows()]
    HeatMap(heatmap_data).add_to(m)
    
    m.save('map.html')
    
if __name__ == '__main__':
    gdf = get_data()
    make_map(gdf)