# services/ftp.py (Installation et configuration du serveur FTP)
import subprocess

def install_ftp(server_ip, ssh_user):
    """
    Installe et configure un serveur FTP (vsftpd) sur le serveur distant via SSH.
    """
    print("Installation du serveur FTP (vsftpd)...")

    ftp_port = input("Port FTP à utiliser (par défaut 21) : ") or "21"

    ftp_config = f"""
    listen=YES
    anonymous_enable=NO
    local_enable=YES
    write_enable=YES
    listen_port={ftp_port}
    """

    try:
        # Installation de vsftpd
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo apt update && sudo apt install -y vsftpd"], check=True)

        # Configuration du serveur FTP
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", f"echo '{ftp_config}' | sudo tee /etc/vsftpd.conf"], check=True)

        # Redémarrage du service FTP
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo systemctl restart vsftpd"], check=True)

        print("Serveur FTP installé et configuré avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation du FTP : {e}")

