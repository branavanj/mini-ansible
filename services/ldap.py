import subprocess

def install_ldap(server_ip, ssh_user):
    """
    Installe et configure un serveur OpenLDAP selon le tutoriel de Server-World.
    
    Ce script réalise les étapes suivantes :
      1. Met à jour la liste des paquets et installe slapd et ldap-utils.
      2. Met à jour le fichier /etc/ldap/ldap.conf pour définir la base (BASE) et l'URI.
      3. Crée un fichier LDIF (/etc/ldap/base.ldif) qui configure la base LDAP
         avec les informations fournies par l'utilisateur.
      4. Applique ce fichier LDIF au serveur LDAP.
    """
    print("Installation du serveur LDAP...")

    # Récupération des informations de configuration
    # On demande à l'utilisateur de saisir le nom de domaine au format LDAP (ex: dc=example,dc=com)
    # et le nom de l'organisation.
    domain_component = input("Nom de domaine en format LDAP (ex: dc=example,dc=com) : ")
    org_name = input("Nom de l'organisation : ")

    # Extraction de la valeur de 'dc' pour le fichier de configuration.
    # Par exemple, pour "dc=example,dc=com", on extrait "example" depuis le premier composant.
    try:
        dc_value = domain_component.split(',')[0].split('=')[1]
    except IndexError:
        print("Erreur de format pour le nom de domaine. Veuillez utiliser le format 'dc=exemple,dc=com'.")
        return

    # Construction du contenu du fichier LDIF de base pour LDAP
    ldap_config = f"""dn: {domain_component}
objectClass: top
objectClass: dcObject
objectClass: organization
o: {org_name}
dc: {dc_value}
"""

    try:
        # 1. Mise à jour des paquets et installation de slapd et ldap-utils
        cmd_install = "sudo apt update && sudo apt install -y slapd ldap-utils"
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", cmd_install], check=True)
        
        # 2. Mise à jour du fichier ldap.conf pour définir BASE et URI
        # On remplace la ligne commençant par BASE et celle commençant par URI.
        cmd_update_conf = (
            f"sudo sed -i 's|^BASE.*|BASE   {domain_component}|' /etc/ldap/ldap.conf && "
            f"sudo sed -i 's|^URI.*|URI    ldap://localhost/|' /etc/ldap/ldap.conf"
        )
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", cmd_update_conf], check=True)
        
        # 3. Création du fichier de configuration de base pour LDAP
        # On envoie le contenu LDIF et on le sauvegarde dans /etc/ldap/base.ldif.
        cmd_create_ldif = f"echo '{ldap_config}' | sudo tee /etc/ldap/base.ldif"
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", cmd_create_ldif], check=True)
        
        # 4. Application de la configuration via ldapadd
        cmd_ldapadd = "sudo ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/base.ldif"
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", cmd_ldapadd], check=True)
        
        print("LDAP installé et configuré avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation du LDAP : {e}")

#
