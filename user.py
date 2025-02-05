
import subprocess
import getpass  

def create_user(server_ip, ssh_user):
    """
    Crée un nouvel utilisateur sur le serveur distant via SSH.
    """
    # Récupérer le nom de l'utilisateur à créer
    username = input("Nom de l'utilisateur à créer : ")

    # Récupérer le mot de passe sans l'afficher (il sera masqué)
    password = getpass.getpass("Mot de passe de l'utilisateur : ")

    # Construction de la commande pour créer l'utilisateur et définir son mot de passe
    # La commande fait deux choses :
    # 1. Créer l'utilisateur avec un dossier personnel et un shell bash.
    # 2. Définir le mot de passe en utilisant chpasswd.
    # Note : Le mot de passe est transmis via la commande echo, mais il n'est pas affiché à l'écran.
    add_user_command = (
        f"sudo useradd -m -s /bin/bash {username} && "
        f"echo '{username}:{password}' | sudo chpasswd"
    )

    try:
        # Exécute la commande SSH sur le serveur distant
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", add_user_command], check=True)
        print(f"Utilisateur {username} créé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur : {e}")

