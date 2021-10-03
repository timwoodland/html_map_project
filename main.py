import pandas as pd
import sys
import folium

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<= elevation <= 3000:
        return 'orange'
    else:
        return 'red'

def main():
    print("Python env is: ", sys.executable)

    m = folium.Map(location=[40.7702, -111.9404], zoom_start=3, tiles="Stamen Terrain")

    vol_fg = folium.FeatureGroup(name="USA Volcanoes")
    pop_fg = folium.FeatureGroup(name="World Popultion")

    df = pd.read_csv("Volcanoes.txt")
    lat = list(df["LAT"])
    lon = list(df["LON"])
    name = list(df["NAME"])
    elev = list(df["ELEV"])

    for lt, ln, n, el in zip(lat, lon, name, elev):
        text = n + "\n Elevation: " + str(el) + "m"
        vol_fg.add_child(folium.CircleMarker(location=[lt, ln],
                                                 radius=10,
                                                 popup=text,
                                                 color=color_producer(el),
                                                 fill_opacity=0.7,
                                                 fill_color=color_producer(el)
                                                 )
                             )

    pop_fg.add_child(folium.GeoJson(data=open('world.json', mode='r', encoding='utf-8-sig'
                                                  ).read(),
                                        style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 1000000
                                        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                        else 'red'}
                                        )
                         )

    m.add_child(pop_fg)
    m.add_child(vol_fg)
    m.add_child(folium.LayerControl())

    m.save("map1.html")

if __name__ == "__main__":
    main()