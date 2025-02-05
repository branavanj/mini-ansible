# connection.py (Gestion de la connexion SSH via ssh user@ip)
import subprocess

def check_connection(server_ip, ssh_user):
    """
    Vérifie si une connexion SSH peut être établie en utilisant ssh user@ip.
    """
    try:
        result = subprocess.run(
            ["ssh", f"{ssh_user}@{server_ip}", "echo Connexion réussie"],
            capture_output=True, text=True, timeout=5
        )
        if "Connexion réussie" in result.stdout:
            print(f"Connexion réussie à {server_ip} en tant que {ssh_user}")
            return True
        else:
            print(f"Erreur : Connexion SSH impossible à {server_ip}")
            return False
    except Exception as e:
        print(f"Erreur de connexion SSH : {e}")
        return False

