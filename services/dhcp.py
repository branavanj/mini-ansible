# services/dhcp.py (Installation et configuration de DHCP via SSH)
import subprocess

def install_dhcp(server_ip, ssh_user):
    """
    Installe et configure le serveur DHCP sur le serveur distant via SSH.
    """

    print("\nInstallation et configuration du serveur DHCP...")

    # Demande des paramètres DHCP
    interface = input("Interface réseau DHCP (ex: ens18) : ")
    domain_name = input("Nom de domaine : ")
    dns_server = input("Nom ou IP du serveur DNS : ")
    subnet = input("Adresse du sous-réseau (ex: 10.0.0.0) : ")
    netmask = input("Masque de sous-réseau (ex: 255.255.255.0) : ")
    gateway = input("Passerelle par défaut : ")
    range_start = input("Plage DHCP - Début (ex: 10.0.0.200) : ")
    range_end = input("Plage DHCP - Fin (ex: 10.0.0.254) : ")

    # Configuration du fichier /etc/default/isc-dhcp-server
    dhcp_defaults_config = f'DHCPDv4_CONF="/etc/dhcp/dhcpd.conf"\nINTERFACESv4="{interface}"'

    # Configuration du fichier /etc/dhcp/dhcpd.conf
    dhcp_config = f"""
option domain-name "{domain_name}";
option domain-name-servers {dns_server};
authoritative;

subnet {subnet} netmask {netmask} {{
    option routers {gateway};
    option subnet-mask {netmask};
    range dynamic-bootp {range_start} {range_end};
}}
"""

    try:
        # Installer le paquet DHCP
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo apt update && sudo apt install -y isc-dhcp-server"], check=True)

        # Modifier /etc/default/isc-dhcp-server
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", f"echo '{dhcp_defaults_config}' | sudo tee /etc/default/isc-dhcp-server"], check=True)

        # Modifier /etc/dhcp/dhcpd.conf
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", f"echo '{dhcp_config}' | sudo tee /etc/dhcp/dhcpd.conf"], check=True)

        # Redémarrer le service DHCP
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo systemctl restart isc-dhcp-server"], check=True)

        print("DHCP installé et configuré avec succès !")
    except Exception as e:
        print(f"Erreur lors de la configuration du DHCP : {e}")

