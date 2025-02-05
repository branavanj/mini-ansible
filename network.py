# network.py (Gestion de la configuration réseau persistante sur Debian via SSH)
import subprocess

def list_network_interfaces(server_ip, ssh_user):
    """
    Liste les interfaces réseau disponibles sur le serveur distant via SSH.
    """
    try:
        result = subprocess.run(
            ["ssh", f"{ssh_user}@{server_ip}", "ip -o link show | awk -F': ' '{print $2}'"],
            capture_output=True, text=True, check=True
        )
        interfaces = result.stdout.strip().split("\n")
        return interfaces
    except Exception as e:
        print(f"Erreur lors de la récupération des interfaces réseau : {e}")
        return []

def configure_network(server_ip, ssh_user):
    """
    Modifie la configuration réseau de manière persistante sur Debian et reconnecte en SSH avec la nouvelle IP.
    """
    interfaces = list_network_interfaces(server_ip, ssh_user)

    if not interfaces:
        print("Impossible de récupérer les interfaces réseau.")
        return

    print("\nInterfaces réseau disponibles :")
    for idx, iface in enumerate(interfaces, 1):
        print(f"{idx} - {iface}")

    try:
        choice = int(input("Choisissez l'interface à configurer (numéro) : ")) - 1
        interface = interfaces[choice]
    except (ValueError, IndexError):
        print("Choix invalide.")
        return

    new_ip = input("Nouvelle adresse IP : ")
    new_gateway = input("Nouvelle passerelle : ")
    new_dns = input("Nouveaux serveurs DNS (séparés par des espaces) : ")

    # Configuration persistante dans /etc/network/interfaces
    network_config = f"""
    auto {interface}
    iface {interface} inet static
        address {new_ip}
        netmask 255.255.255.0
        gateway {new_gateway}
        dns-nameservers {new_dns}
    """

    try:
        # Écriture dans /etc/network/interfaces
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", f"echo '{network_config}' | sudo tee /etc/network/interfaces"], check=True)

        # Redémarrer le service réseau pour appliquer la configuration
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo systemctl restart networking"], check=True)

        print(f"Configuration réseau appliquée avec succès sur {interface}.")

        # Fermer l'ancienne connexion SSH et relancer avec la nouvelle IP
        print(f"Reconnexion au serveur avec la nouvelle IP : {new_ip}")
        subprocess.run(["ssh", f"{ssh_user}@{new_ip}"])

    except Exception as e:
        print(f"Erreur lors de la modification du réseau : {e}")

