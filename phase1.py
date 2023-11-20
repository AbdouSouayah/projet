"""Phase1"""
import argparse
import json
from datetime import date, datetime
import requests
def parse_args():
    """module parse_args"""
    parser = argparse.ArgumentParser(
        description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers."
    )

    parser.add_argument(
        "symbole", nargs="+", help="Nom d'un symbole boursier"
    )
    parser.add_argument(
        "-d", "--debut", type=str, metavar="DATE",
        help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)"
    )
    parser.add_argument(
        "-f", "--fin", type=str, metavar="DATE",
        help="Date recherchée la plus récente (format: AAAA-MM-JJ)"
    )
    parser.add_argument(
        "-v",
        "--valeur",
        choices=["fermeture", "ouverture", "min", "max", "volume"],
        default="fermeture",
        help="La valeur désirée (par défaut: fermeture)",
    )

    return parser.parse_args()

def get_start_date(date_debut):
    """module de date de debut"""
    return date_debut or str(date.today())

def get_end_date(date_fin):
    """module de date de fin"""
    return date_fin or str(date.today())

def get_historical_data(symbol, start_date, end_date, value_type):
    """module historical"""
    url = f'https://pax.ulaval.ca/action/{symbol}/historique/'

    params = {
        'début': start_date,
        'fin': end_date,
    }

    response = requests.get(url=url, params=params)

    if response.status_code == 200:
        data = json.loads(response.text)
        historical_data = data.get('historique', {})

        if start_date and end_date:
            historical_data = {
                datetime.strptime(date, "%Y-%m-%d").date(): values.get(value_type, None)
                for date, values in historical_data.items()
            }

        if value_type == "volume":
            historical_data = {
                date: volume
                for date, volume in historical_data.items() if volume is not None
            }

        return historical_data
def format_date(date_str):
    """convertir en datetime"""
    if isinstance(date_str, str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_obj.strftime("datetime.date(%Y, %m, %d)")
    return date_str

def format_date1(date_obj):
    """convertir en datetime"""
    return f"datetime.date({date_obj.year}, {date_obj.month}, {date_obj.day})"

def main():
    """affichage"""
    args = parse_args()
    start_date = get_start_date(args.debut)
    end_date = get_end_date(args.fin)

    for symbol in args.symbole:
        if args.valeur == "volume" and args.fin:
            historical_data = get_historical_data(symbol, args.fin, args.fin, args.valeur)
        else:
            historical_data = get_historical_data(symbol, start_date, end_date, args.valeur)

        if historical_data:
            if args.valeur == "volume":
                a = format_date(end_date)
                print(f"titre={symbol}: valeur=volume, début={a}, fin={a}")
                for Date, volume in historical_data.items():
                    print(f"[({format_date1(Date)}, {volume})]")
            else:
                a=format_date(start_date)
                b=format_date(end_date)
                print(f"titre={symbol}: valeur={args.valeur}, début={a}, fin={b}")
                sorted_data = sorted(historical_data.items())
                print(sorted_data)

if __name__ == "__main__":
    main()
