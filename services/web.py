# services/web.py (Installation et configuration du serveur Web)
import subprocess

def install_web(server_ip, ssh_user):
    """
    Installe et configure un serveur Web (Apache) sur le serveur distant via SSH.
    """
    print("Installation du serveur Web (Apache)...")

    web_port = input("Port HTTP à utiliser (par défaut 80) : ") or "80"
    enable_https = input("Activer HTTPS ? (o/n) : ").lower() == "o"

    apache_config = f"""
    Listen {web_port}
    <VirtualHost *:{web_port}>
        DocumentRoot /var/www/html
    </VirtualHost>
    """

    try:
        # Installation d'Apache
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo apt update && sudo apt install -y apache2"], check=True)

        # Configuration du port et du vhost
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", f"echo '{apache_config}' | sudo tee /etc/apache2/sites-available/000-default.conf"], check=True)

        if enable_https:
            subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo a2enmod ssl && sudo systemctl restart apache2"], check=True)

        # Redémarrage d'Apache
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo systemctl restart apache2"], check=True)

        print("Serveur Web installé et configuré avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation du serveur Web : {e}")

