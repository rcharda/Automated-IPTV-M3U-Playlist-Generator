import os
import requests

def generate_vavoo_m3u():
    print("Connexion à l'API officielle de Vavoo...")
    url = "https://vavoo.to"
    headers = {
        "User-Agent": "VAVOO/2.6",
        "Accept": "application/json",
        "X-VAVOO-Device": "vavoo_box"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"Erreur de connexion : Code {response.status_code}")
            return
            
        channels = response.json()
        if not isinstance(channels, list):
            print("Le format renvoyé par Vavoo est incorrect.")
            return

        # Dossiers cibles trouvés dans l'arborescence de ton dépôt
        paths = ["LiveTV/Mikhoul", "BugsfreeMain/LiveTV/Mikhoul"]
        
        for folder in paths:
            os.makedirs(folder, exist_ok=True)
            output_file = os.path.join(folder, "LiveTV.m3u")
            
            print(f"Écriture de {len(channels)} chaînes dans : {output_file}")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for channel in channels:
                    channel_id = channel.get("id")
                    if not channel_id:
                        continue
                    name = channel.get("name", "Chaîne Inconnue")
                    group = channel.get("group", "Vavoo Live")
                    logo = channel.get("logo", "")
                    
                    # Lien de streaming direct traité à la volée par l'API Vavoo
                    stream_url = f"https://vavoo.to{channel_id}.m3u8"
                    
                    f.write(f'#EXTINF:-1 tvg-id="{channel_id}" tvg-logo="{logo}" group-title="{group}",{name}\n')
                    f.write(f"{stream_url}\n")
                    
        print("Mise à jour globale terminée avec succès !")

    except Exception as e:
        print(f"Une erreur critique est survenue : {e}")

if __name__ == "__main__":
    generate_vavoo_m3u()
