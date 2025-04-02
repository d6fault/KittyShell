



# KittyShell - Reverse Shell Listener 💀

**KittyShell** is a simple reverse shell listener designed to listen for incoming reverse shell connections. It supports SSL encryption for secure communication between the server and the client.

This tool is made with love ❤️ by **D6fault**.

## Features
- Listens for incoming reverse shell connections from the client.
- Supports SSL encryption to secure communication.
- Customizable IP address and port.
- Command execution and output display on the listener side.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/d6fault/KittyShell.git
   cd KittyShell
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   - `colorama`: For colorful terminal output.
   - `ssl`: For supporting secure SSL connections.

3. Make sure you have Python 3.x installed.

## Usage

To use **KittyShell** as a reverse shell listener, run the following command:

```bash
python3 kittyshell.py -i <IP_ADDRESS> -p <PORT> [-s]
```

### Arguments:
- `-i` or `--host` - The host IP address to listen on (default is `0.0.0.0`).
- `-p` or `--port` - The port to listen on (default is `4444`).
- `-s` or `--ssl` - Optional flag to enable SSL encryption for the communication.

### Example:
To listen on IP address `192.168.1.100` and port `4444` with SSL encryption enabled, use the following command:

```bash
python3 kittyshell.py -i 192.168.1.100 -p 4444 -s
```

If you don’t need SSL, omit the `-s` flag:

```bash
python3 kittyshell.py -i 192.168.1.100 -p 4444
```

## How It Works

1. **Start the listener**: Use the provided command to start the listener on a specific IP and port.
2. **Wait for incoming connection**: The listener waits for a reverse shell connection from the client.
3. **Command interaction**: Once the connection is established, you can issue commands to the client. The output will be displayed in the terminal.
4. **Exit**: Type `exit` to close the connection.

## Security Notice
Please use **KittyShell** only in a secure and authorized environment. Unauthorized use of reverse shells can be illegal and unethical. Always have explicit permission before using such tools.

## Contributing

Contributions are welcome! Feel free to fork the repository and create pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

### Planned Features for KittyShell:

- [ ] **Firewall Detection**  
  - [ ] Detect if the client is behind a firewall.
  - [ ] Provide feedback on firewall status.
  - [ ] Attempt to bypass common firewall configurations.

- [ ] **Security Software Detection**  
  - [ ] Detect antivirus or security software running on the target system.
  - [ ] Provide alerts when security software is found.
  - [ ] Implement methods to bypass or disable security software (if possible).

- [ ] **Linux Persistence**  
  - [ ] Create cron jobs to maintain access on Linux machines.
  - [ ] Modify system startup files (e.g., `/etc/rc.local` or `~/.bashrc`) for persistence.
  
- [ ] **Windows Persistence**  
  - [ ] Add registry entries to maintain access on Windows systems.
  - [ ] Create scheduled tasks to ensure reverse shell persists after reboots.

---

