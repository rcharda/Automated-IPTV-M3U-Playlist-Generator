import os
import requests

def generate_vavoo_m3u():
    print("Connexion au serveur miroir d'écosystème Vavoo/Oha...")
    
    # Liste de serveurs miroirs stables et publics pour l'écosystème Vavoo/Oha/Koto
    sources = [
        "https://github.io", # Source FR stable mondiale
        "https://githubusercontent.com", # Secours Vavoo
        "https://vavoo.to" # API Directe en dernier recours
    ]
    
    m3u_content = ""
    for url in sources:
        try:
            print(f"Tentative de récupération depuis : {url}")
            headers = {"User-Agent": "VAVOO/2.6"} if "vavoo" in url else {}
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Si c'est l'API JSON brute de Vavoo, on la convertit en M3U
                if url.endswith("/index"):
                    channels = response.json()
                    m3u_content = "#EXTM3U\n"
                    for c in channels:
                        if c.get("id"):
                            m3u_content += f'#EXTINF:-1 tvg-id="{c["id"]}" group-title="{c.get("group", "Vavoo")}",{c.get("name")}\n'
                            m3u_content += f'https://vavoo.to{c["id"]}.m3u8\n'
                else:
                    m3u_content = response.text
                
                if m3u_content.startswith("#EXTM3U"):
                    print("=> Flux récupérés avec succès !")
                    break
        except Exception as e:
            print(f"Échec de cette source : {e}")
            continue

    if not m3u_content:
        print("Erreur : Impossible de récupérer les chaînes depuis toutes les sources.")
        return

    # Sauvegarde dans ton arborescence GitHub
    paths = ["LiveTV/Mikhoul", "BugsfreeMain/LiveTV/Mikhoul"]
    for folder in paths:
        os.makedirs(folder, exist_ok=True)
        output_file = os.path.join(folder, "LiveTV.m3u")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"Fichier mis à jour dans : {output_file}")

if __name__ == "__main__":
    generate_vavoo_m3u()
