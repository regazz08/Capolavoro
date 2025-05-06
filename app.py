import requests
from tabulate import tabulate
from colorama import Fore, Style, init

# Inizializza colorama per supportare i colori nel terminale
init(autoreset=True)

#In base alla descrizione del meteo, restituisce l'icona corrispondente
def get_icone(descrizione):
    icone = {
        'sereno': '☀️ ',
        'nuvole': '☁️ ',
        'pioggia': '🌧️ ',
        'neve': '❄️ ',
        'temporale': '⛈️ ',
        'pioggerella': '🌦️ ',
        'nebbia': '🌫️ '
    }
    desc = descrizione.lower()
    for chiave in icone:
        if chiave in desc:
            return icone[chiave]
    return '🌤️'

# Funzione per ottenere i dati meteo attuali

def get_attuale(citta, api):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={citta}&appid={api}&units=metric&lang=it"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "temperatura": data["main"]["temp"],
            "descrizione": data["weather"][0]["description"],
            "umidita": data["main"]["humidity"],
            "pressione": data["main"]["pressure"],
            "vento": data["wind"]["speed"]
        }
    return None

# funxioni per le previsioni per i prossimi 5 giorni
def get_previsioni(citta, api):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={citta}&appid={api}&units=metric&lang=it"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        previsioni = []
        for forecast in data["list"][:5]:
            previsioni.append({
                "data": forecast["dt_txt"].split(" ")[0],
                "temperatura": forecast["main"]["temp"],
                "descrizione": forecast["weather"][0]["description"],
            })
        return previsioni
    return [{}] * 5

# Funzione per mostrare i dati meteo attuali
def mostra_meteo_attuale(citta, api):
    attuale_data = get_attuale(citta, api)
    if attuale_data:
        attuale_data["icona"] = get_icone(attuale_data["descrizione"])
        
        print(Fore.RED + "\n" + "═" * 100)
        print(Fore.RED + " METEO ATTUALE ".center(100, " "))
        print(Fore.RED + "═" * 100)
        
        meteo_attuale = [
            [Fore.GREEN + "🌡️ TEMPERATURA", f"{Fore.WHITE}{attuale_data['temperatura']}°C" ],
            [Fore.CYAN + "💧 UMIDITÀ", f"{Fore.WHITE}{attuale_data['umidita']}%" ],
            [Fore.MAGENTA + "⛅ DESCRIZIONE", f"{attuale_data['icona']} {Fore.WHITE}{attuale_data['descrizione'].title()}" ],
            [Fore.YELLOW + "📊 PRESSIONE", f"{Fore.WHITE}{attuale_data['pressione']} hPa" ],
            [Fore.WHITE + "💨 VENTO", f"{Fore.WHITE}{attuale_data['vento']} m/s" ]
        ]
        
        print(tabulate(meteo_attuale, tablefmt="fancy_grid"))
    else:
        print(Fore.RED + "Errore nel recupero dei dati attuali.")

# Funzione per mostrare le previsioni
def mostra_previsioni(citta, api):
    previsioni = get_previsioni(citta, api)
    
    print(Fore.RED + "\n" + "═" * 100)
    print(Fore.RED + " PREVISIONI  ".center(100, " "))
    print(Fore.RED + "═" * 100)
    
    previsione_data = []
    for previsione in previsioni:
        if previsione:
            icona = get_icone(previsione['descrizione'])
            previsione_data.append([
                f"{Fore.YELLOW}{previsione['data']}",
                f"{Fore.WHITE}{previsione['temperatura']}°C",
                f"{icona} {Fore.WHITE}{previsione['descrizione'].title()}"
            ])
        else:
            previsione_data.append([f"{Fore.BLUE}N/D", f"{Fore.YELLOW}N/D", f"{Fore.MAGENTA}N/D"])
    
    print(tabulate(previsione_data, 
                  headers=[f"{Fore.YELLOW}DATA", f"{Fore.WHITE}TEMPERATURA", f"{Fore.WHITE}CONDIZIONI"],
                  tablefmt="fancy_grid"))

# Funzione principale

api = "7bf8066ca24288fd0bd382cb09ac39c2"# API key di OpenWeatherMap

#Print del titolo
print(Fore.CYAN + "\n" + "=" * 100)
print(Fore.RED + " METEO APP ".center(100, "="))
print(Fore.CYAN + "=" * 100)
    
citta = input("\nInserisci la città per la quale vuoi conoscere il meteo: ")#richiedo città
    
#scelta dell'opzione
print(Fore.CYAN + "\n" + "=" * 100)
print("Scegli un'opzione:")
print(Fore.GREEN + "1. Meteo attuale")
print(Fore.BLUE + "2. Prossime 5 previsioni")
print(Fore.MAGENTA + "3. Entrambi")
print(Fore.WHITE + "0. Esci")
print(Fore.CYAN +"\n"+"=" * 100)
       

flag=True
while flag==True:
    scelta = input("\nCosa desideri conoscere(premi 0 per uscire): ")
    if scelta == "1":
        mostra_meteo_attuale(citta, api)
    elif scelta == "2":
        mostra_previsioni(citta, api)
    elif scelta == "3":
        mostra_meteo_attuale(citta, api)
        mostra_previsioni(citta, api)
    elif scelta == "0":
        flag==False
        print(Fore.CYAN + "=" * 100)
        print(Fore.CYAN + "\nGrazie per aver usato la mia applicazione per visualizzare il meteo")
        print(Fore.CYAN + "=" * 100)
        exit
    else:
        print(Fore.RED + "\nScegli un opzione valida")
        flag==False
        

