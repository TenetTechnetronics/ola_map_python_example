import requests
import folium
import tkinter as tk
from tkinter import messagebox
import webbrowser

def generate_map():
    search_text = search_entry.get()
    api_key = api_key_entry.get()
    
    if not search_text or not api_key:
        messagebox.showerror("Input Error", "Please enter both search text and API key.")
        return
    
    url = f"https://api.olamaps.io/places/v1/autocomplete?input={search_text}&api_key={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Check if the response contains predictions
        if 'predictions' in data:
            predictions = data['predictions']
            
            # Sort the predictions by distance (if available)
            sorted_predictions = sorted(predictions, key=lambda x: x.get('distance_meters', float('inf')))
            
            # Create a map centered around the first location
            first_location = sorted_predictions[0]['geometry']['location']
            map_center = [first_location['lat'], first_location['lng']]
            m = folium.Map(location=map_center, zoom_start=14)
            
            # Print the sorted predictions in a readable manner and add to map
            for idx, prediction in enumerate(sorted_predictions, 1):
                main_text = prediction['structured_formatting']['main_text']
                secondary_text = prediction['structured_formatting']['secondary_text']
                distance = prediction.get('distance_meters', 'N/A')
                place_id = prediction.get('place_id', 'N/A')
                description = prediction.get('description', 'N/A')
                location = prediction.get('geometry', {}).get('location', {})
                lat = location.get('lat', 'N/A')
                lng = location.get('lng', 'N/A')
                types = ', '.join(prediction.get('types', []))
                matched_substrings = ', '.join([f"offset: {ms['offset']}, length: {ms['length']}" for ms in prediction.get('matched_substrings', [])])
                terms = ', '.join([term['value'] for term in prediction.get('terms', [])])
                
                print(f"{idx}. {main_text} ({distance} meters away)\n"
                      f"   Secondary Text: {secondary_text}\n"
                      f"   Place ID: {place_id}\n"
                      f"   Description: {description}\n"
                      f"   Location: lat {lat}, lng {lng}\n"
                      f"   Types: {types}\n"
                      f"   Matched Substrings: {matched_substrings}\n"
                      f"   Terms: {terms}\n")
                
                # Add marker to the map
                folium.Marker(
                    location=[lat, lng],
                    popup=f"{main_text}\n{secondary_text}",
                    tooltip=f"{main_text} ({distance} meters away)"
                ).add_to(m)
            
            # Save the map to an HTML file
            map_file = "map.html"
            m.save(map_file)
            print(f"Map has been saved to {map_file}")
            
            # Open the map.html file in the default web browser
            webbrowser.open(map_file)
            
        else:
            print("No predictions found.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Create the Tkinter window
root = tk.Tk()
root.title("Map Generator")
root.geometry("400x200")

# Create and place widgets
tk.Label(root, text="Search Text:").pack(pady=5)
search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

tk.Label(root, text="API Key:").pack(pady=5)
api_key_entry = tk.Entry(root, width=50)
api_key_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Map", command=generate_map)
generate_button.pack(pady=20)

root.mainloop()
