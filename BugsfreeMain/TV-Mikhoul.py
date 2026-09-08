import os
import requests
import re

def generate_vavoo_m3u():
    print("Connexion au miroir de secours Vavoo...")
    # Utilisation d'un index brut alternatif pour contourner le blocage Cloudflare sur GitHub
    url = "https://githubusercontent.com"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            print(f"Erreur de connexion au miroir : Code {response.status_code}")
            return
            
        m3u_content = response.text
        if not m3u_content.startswith("#EXTM3U"):
            print("Le fichier récupéré n'est pas une playlist valide.")
            return

        # Dossiers cibles sur ton dépôt
        paths = ["LiveTV/Mikhoul", "BugsfreeMain/LiveTV/Mikhoul"]
        
        for folder in paths:
            os.makedirs(folder, exist_ok=True)
            output_file = os.path.join(folder, "LiveTV.m3u")
            
            print(f"Écriture et conversion de la playlist dans : {output_file}")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(m3u_content)
                    
        print("Mise à jour globale terminée avec succès !")

    except Exception as e:
        print(f"Une erreur critique est survenue : {e}")

if __name__ == "__main__":
    generate_vavoo_m3u()
