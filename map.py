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
    m = folium.Map(location=[gdf.iloc[1]['Lat'], gdf.iloc[1]['Lon']],tiles=None, zoom_start=6)
    ftr_grp1 = folium.FeatureGroup(name='Verse Locations')
    ftr_grp2 = folium.FeatureGroup(name='Heat Map')
    tile_layer = folium.TileLayer(tiles=MAPBOX_API,
                                  min_zoom=0,
                                  max_zoom=26,
                                  attr='<a href=https://ebible.org/>© eBible</a> | <a href=http://www.openbible.info/>© OpenBible</a> | <a href=https://www.mapbox.com/about/maps/>© Mapbox</a>',
                                  name='Mapbox Satellite')
    #points = folium.features.GeoJson(gdf)
    
    for i in range(len(gdf)):
        X = gdf.iloc[i]['Lat']
        Y = gdf.iloc[i]['Lon']
        if str(gdf.iloc[i]['Root']) == np.nan:
               verse = str(gdf.iloc[i]['#ESV'])+'\n'+str(gdf.iloc[i]['Root'])
        else:
            verse = str(gdf.iloc[i]['#ESV'])
            
        folium.CircleMarker([X, Y], radius=2, weight=4, popup=folium.Popup(verse)).add_to(ftr_grp1)
        
    heatmap_data = [[row['Lat'], row['Lon']] for index, row in gdf.iterrows()]
    HeatMap(heatmap_data).add_to(ftr_grp2)
    
    m.add_child(tile_layer)
    m.add_child(ftr_grp1)
    m.add_child(ftr_grp2)
    m.add_child(folium.map.LayerControl(position='topright', collapsed=True))
    m.save('map.html')
    
if __name__ == '__main__':
    gdf = get_data()
    make_map(gdf)
