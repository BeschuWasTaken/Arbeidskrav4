# Importerer nødvendige biblioteker
import serial
import sys
import time

# Setter timeout for serielle data
READ_TIMEOUT = 8

# Henter brukerinput om operativsystem og konfigurasjon
OperatingSystem = input('\nWhich operating system are you connecting from? (W or L) ->')
SerialPortNumber = input('\nEnter serial port number ->')
Hostname = input('\nEnter desired hostname ->')

# Trunk-portvalg
TrunkQuery = input('\nDo you want trunk ports? (y or n) ->')
if TrunkQuery in ("y", "Y", "yes", "Yes"):
	TrunkQuery2 = input('\nDo you want a single trunk port or a range? (single/range) ->')
	if TrunkQuery2 in ("single", "Single"):
		TrunkPort = input('\nEnter trunk port (ex. Gig1/0/1) ->')
	elif TrunkQuery2 in ("range", "Range"):
		TrunkPortRange = input('\nEnter trunk port range (ex. Gig1/0/1-2) ->')
	else:
		print("Invalid input")

# Management-portvalg
MGMTQuery = input('\nDo you want a management port? (y or n) ->')
if MGMTQuery in ("y", "Y", "yes", "Yes"):
	MGMTPort = input('\nEnter management port number (ex. Gig1/0/1) ->')

# VLAN, IP og brukerinformasjon
MGMTVLAN = input('\nEnter management VLAN number ->')
IPAddress = input('\nEnter desired IP address AND subnet mask->')
SSHUsername = input('\nEnter SSH Username ->')
SSHSecret = input('\nEnter SSH Password ->')
EnableSecret = input('\nEnter Enable Password ->')

# Definerer serielle portnavn basert på operativsystem
SerialPortNameLinux = '/dev/ttyS' + SerialPortNumber
SerialPortNameWindows = 'COM' + SerialPortNumber

# Lager kommandoer som skal sendes til enheten via seriell
HostnameString = 'hostname ' + Hostname + '\r\n'
if MGMTQuery in ("y", "Y", "yes", "Yes"):
	MGMTPortString = 'int ' + MGMTPort + '\r\n'
	MGMTConfig = 'switchport access vlan ' + MGMTVLAN + '\r\n'
MGMTVLANString = 'int vlan ' + MGMTVLAN + '\r\n'
IPAddressString = 'ip address ' + IPAddress + '\r\n'
MGMTVLANCreateString = 'vlan ' + MGMTVLAN + '\r\n'
SSHCredentials = 'username ' + SSHUsername + ' privilege 15 secret ' + SSHSecret + '\r\n'
EnableSecretString = 'enable secret ' + EnableSecret + '\r\n'

# Trunk-konfig basert på input
if TrunkQuery in ("y", "Y", "yes", "Yes"):
	if TrunkQuery2 in ("single", "Single"):
		TrunkPortConfig = 'int ' + TrunkPort + '\r\n'
	elif TrunkQuery2 in ("range", "Range"):
		TrunkPortRangeConfig = 'int range ' + TrunkPortRange + '\r\n'

# Hovedfunksjonen som setter opp svitsjen via seriell tilkobling
def main():
	print("\nInitializing serial connection") 

	# Åpner riktig seriell port basert på OS
	if OperatingSystem in ("l", "L", "linux", "Linux"):
		console = serial.Serial(
			port=SerialPortNameLinux,
			baudrate=9600,
			parity="N",
			stopbits=1,
			bytesize=8,
			timeout=READ_TIMEOUT
		)
	elif OperatingSystem in ("w", "W", "windows", "Windows"):
		console = serial.Serial(
			port=SerialPortNameWindows,
			baudrate=9600,
			parity="N",
			stopbits=1,
			bytesize=8,
			timeout=READ_TIMEOUT
		)
	else:
		print("Invalid input")

	# Skriver ut valgt port
	print(console.name)

	# Avslutt om porten ikke er åpen
	if not console.isOpen():
		sys.exit()
	
	# Sender innledende kommandoer
	console.write("\r\n\r\n\r\n".encode())
	console.write("enable\r\n".encode())
	console.write("conf t\r\n".encode())

	# Leser og viser eventuell respons
	input_data = console.read(console.inWaiting())
	print(input_data)

	# Konfigurerer hostname og VLAN
	console.write(HostnameString.encode())
	console.write(MGMTVLANString.encode())
	console.write(IPAddressString.encode())
	console.write("no shutdown\r\n".encode())
	console.write("exit\r\n".encode())

	# Oppretter VLAN og setter navn
	console.write(MGMTVLANCreateString.encode())
	console.write("name MGMT\r\n".encode())
	console.write("exit\r\n".encode())

	# Konfigurerer eventuell management-port
	if MGMTQuery in ("y", "Y", "yes", "Yes"):
		console.write(MGMTPortString.encode())
		console.write("switchport mode access\r\n".encode())
		console.write(MGMTConfig.encode())
		console.write("no shutdown\r\n".encode())
		time.sleep(2)
		console.write("exit\r\n".encode())
	
	# Konfigurerer trunk-port(er) hvis valgt
	if TrunkQuery in ("y", "Y", "yes", "Yes"):
		if TrunkQuery2 in ("single", "Single"):
			console.write(TrunkPortConfig.encode())
		elif TrunkQuery2 in ("range", "Range"):
			console.write(TrunkPortRangeConfig.encode())
		console.write("switchport mode trunk\r\n".encode())
		console.write("exit\r\n".encode())
	
	# Konfigurerer domenenavn og genererer RSA-nøkkel
	console.write("ip domain name mynetwork.local\r\n".encode())
	console.write("crypto key generate rsa modulus 1024\r\n".encode())

	# Leser eventuelle meldinger (f.eks. bekreftelser)
	input_data = console.read(console.inWaiting())
	print(input_data)
	time.sleep(3)

	# Setter opp SSH-tilgang
	console.write(SSHCredentials.encode())
	console.write("line vty 0 15\r\n".encode())
	console.write("transport input ssh\r\n".encode())
	console.write("login local\r\n".encode())
	console.write("exec-timeout 60 0\r\n".encode())
	console.write("exit\r\n".encode())

	# Setter enable-passord
	console.write(EnableSecretString.encode())

	# Leser siste respons
	input_data = console.read(console.inWaiting())
	print(input_data)

# Starter programmet hvis scriptet kjøres direkte
if __name__ == "__main__":
	main()