# services/dns.py (Installation et configuration de DNS via SSH)
import subprocess

def install_dns(server_ip, ssh_user):
    """
    Installe et configure un serveur DNS (Bind9).
    """
    print("Installation du serveur DNS...")

    domain_name = input("Nom de domaine : ")
    zone_direct = f"/etc/bind/db.{domain_name}"

    zone_config = f"""
    zone "{domain_name}" {{
        type master;
        file "{zone_direct}";
    }};
    """

    dns_zone_data = f"""
    $TTL 86400
    @ IN SOA ns.{domain_name}. admin.{domain_name}. (
        2024010101  ; Serial
        3600        ; Refresh
        1800        ; Retry
        604800      ; Expire
        86400       ; Minimum TTL
    )
    @ IN NS ns.{domain_name}.
    ns IN A {server_ip}
    """

    try:
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo apt update && sudo apt install -y bind9"], check=True)
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", f"echo '{zone_config}' | sudo tee /etc/bind/named.conf.local"], check=True)
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", f"echo '{dns_zone_data}' | sudo tee {zone_direct}"], check=True)
        subprocess.run(["ssh", f"{ssh_user}@{server_ip}", "sudo systemctl restart bind9"], check=True)
        print("DNS installé et configuré avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation du DNS : {e}")

