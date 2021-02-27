import folium
import sqlite3
import numpy as np
import pandas as pd
import geopandas as gpd
from folium import plugins
from folium.plugins import HeatMap
from MAPBOX_API import MAPBOX_API

def get_data():
    db = sqlite3.connect('./Data/BIBLE.db')
    df = pd.read_sql_query('SELECT * FROM KJV', db)
    dfwiki = pd.read_sql_query('SELECT * FROM WIKI', db)
    dflocs = pd.read_sql_query('SELECT * FROM LOCATIONS', db)
    
    gdf = gpd.GeoDataFrame(dflocs, geometry=gpd.points_from_xy(dflocs.LONG, dflocs.LAT))
    gdf = gdf.set_crs(epsg=4326, inplace=True)
    return gdf, df, dfwiki

def make_map(gdf, df):
    m = folium.Map(location=[gdf.iloc[1]['LAT'], gdf.iloc[1]['LONG']],tiles=None, zoom_start=6)
    ftr_grp1 = folium.FeatureGroup(name='Verse Locations')
    ftr_grp2 = folium.FeatureGroup(name='Heat Map')
    tile_layer = folium.TileLayer(tiles=MAPBOX_API,
                                  min_zoom=0,
                                  max_zoom=26,
                                  attr='<a href=https://ebible.org/>© eBible</a> | <a href=http://www.openbible.info/>© OpenBible</a> | <a href=https://www.mapbox.com/about/maps/>© Mapbox</a>',
                                  name='Mapbox Satellite')
    #points = folium.features.GeoJson(gdf)
    
    for i in range(len(gdf)):
        X = gdf.iloc[i]['LAT']
        Y = gdf.iloc[i]['LONG']
        if str(gdf.iloc[i]['NAME2']) is not True:
               loc_name = str(gdf.iloc[i]['NAME1'])+' - '+str(gdf.iloc[i]['NAME2'])
        else:
            loc_name = str(gdf.iloc[i]['NAME1'])

        verse_no = str(gdf.iloc[i]['BOOK'])+' '+str(gdf.iloc[i]['CHAPTER'])+':'+str(gdf.iloc[i]['VERSE'])
        verse_text = str(gdf.iloc[i]['TEXT'])
        popup_text = str(loc_name+' ¦¦ '+verse_no+' ¦¦ '+'"'+verse_text+'"')
        
        folium.CircleMarker([X, Y], radius=2, weight=4, popup=folium.Popup(popup_text, max_width=500)).add_to(ftr_grp1)
        
    heatmap_data = [[row['LAT'], row['LONG']] for index, row in gdf.iterrows()]
    HeatMap(heatmap_data).add_to(ftr_grp2)
    
    title = '<title>Bible Map App</title>'
    m.get_root().html.add_child(folium.Element(title))
    
    m.add_child(tile_layer)
    m.add_child(ftr_grp1)
    m.add_child(ftr_grp2)
    m.add_child(folium.map.LayerControl(position='topright', collapsed=True))
    m.save('map.html')
    
if __name__ == '__main__':
    gdf, df, dfwiki = get_data()
    make_map(gdf, df)