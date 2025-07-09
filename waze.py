import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "f4a1cfc4-0825-4ea1-9060-732337cc4a94"  # Reemplaza con tu propia API key

def input_con_salida(mensaje):
    entrada = input(f"{mensaje} (o presiona 's' para salir): ")
    if entrada.lower() == "s":
        print("Saliendo del programa.")
        exit()
    return entrada

def geocoding(location, key):
    while location == "":
        location = input_con_salida("Ingrese nuevamente la localización")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        print(f"API URL para {new_loc} (Location Type: {value})\n{url}")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print(f"Estado de la API: {json_status}\nError message: {json_data['message']}")
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfil del vehículo en Graphhopper: car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")

    profile = ["car", "bike", "foot"]
    vehicle = input_con_salida("Ingrese uno de los perfiles de transporte mostrados en la lista anterior")
    if vehicle not in profile:
        print("No se ha ingresado ningún perfil válido. Se usará el perfil car.")
        vehicle = "car"

    loc1 = input_con_salida("Ciudad de origen")
    orig = geocoding(loc1, key)

    loc2 = input_con_salida("Ciudad de Destino")
    dest = geocoding(loc2, key)

    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print(f"Estado de la API de enrutamiento: {paths_status}\nRouting API URL:\n{paths_url}")
        print("=================================================")
        print(f"Indicaciones desde {orig[3]} hasta {dest[3]} mediante {vehicle}")
        print("=================================================")

        if paths_status == 200:
            distance_m = paths_data["paths"][0]["distance"]
            time_ms = paths_data["paths"][0]["time"]
            miles = distance_m / 1000 / 1.61
            km = distance_m / 1000
            sec = int(time_ms / 1000 % 60)
            min = int(time_ms / 1000 / 60 % 60)
            hr = int(time_ms / 1000 / 60 / 60)

            print(f"Distancia viajada: {miles:.1f} millas / {km:.1f} km")
            print(f"Duración del viaje: {hr:02d}:{min:02d}:{sec:02d}")

            try:
                consumo_promedio = float(input_con_salida("Ingrese el consumo promedio de combustible (litros por 100 km)"))
                combustible_requerido = km * (consumo_promedio / 100)
                print(f"Combustible requerido para el viaje: {combustible_requerido:.2f} litros")
            except ValueError:
                print("Entrada inválida para el consumo promedio. No se pudo calcular el combustible requerido.")

            print("=================================================")
            for each in paths_data["paths"][0]["instructions"]:
                path = each["text"]
                distance = each["distance"]
                print(f"{path} ( {distance/1000:.1f} km / {distance/1000/1.61:.1f} miles )")
                print("=============================================")
        else:
            print("Mensaje de Error: " + paths_data["message"])
        print("*************************************************")