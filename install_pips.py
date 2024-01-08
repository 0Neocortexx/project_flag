import sys
import subprocess
import time

def install_pips():
    # instalando pips em segundo plano
    pips = ['flask_sqlalchemy', 'flask','flask_cors', 'flask_jwt_extended', 'bcrypt', 'timedelta']
    for a in pips:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', a])

# Corrigir atualizacaos pip
def verify_updates():
    # atualizando pips
    pips = ['flask_sqlalchemy']
    for b in pips:
        subprocess.check_call([sys.executable, '-m','pip', 'install', b, '--upgrade pip'])
        time.sleep(1)
        print("Instalando pacotes ...")
    time.sleep(1)
    print("Pacotes instalados!")



install_pips()