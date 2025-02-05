# main.py (Point d'entrée principal)
import connection
import network
import user
from services import dhcp, dns, ldap, ftp, web

def main():
    server_ip = input("Entrez l'IP du serveur à administrer : ")
    ssh_user = input("Entrez le nom d'utilisateur SSH : ")

    if not connection.check_connection(server_ip, ssh_user):
        print("Erreur : Connexion SSH impossible.")
        return
    
    while True:
        print("\nQue voulez-vous faire ?")
        print("1 - Changer la configuration réseau")
        print("2 - Installer et configurer un service")
        print("3 - Créer un utilisateur")
        print("4 - Quitter")
        
        choix = input("Votre choix : ")
        
        if choix == "1":
            network.configure_network(server_ip, ssh_user)
        elif choix == "2":
            print("\nQuel service installer ?")
            print("1 - DHCP")
            print("2 - DNS")
            print("3 - LDAP")
            print("4 - FTP")
            print("5 - Web")
            service_choix = input("Votre choix : ")
            
            if service_choix == "1":
                dhcp.install_dhcp(server_ip, ssh_user)
            elif service_choix == "2":
                dns.install_dns(server_ip, ssh_user)
            elif service_choix == "3":
                ldap.install_ldap(server_ip, ssh_user)
            elif service_choix == "4":
                ftp.install_ftp(server_ip, ssh_user)
            elif service_choix == "5":
                web.install_web(server_ip, ssh_user)
            else:
                print("Choix invalide.")
        elif choix == "3":
            user.create_user(server_ip, ssh_user)
        elif choix == "4":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()

