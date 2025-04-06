# Importerer nødvendige biblioteker
import serial
import sys
import time

# Setter timeout for serielle data
READ_TIMEOUT = 8

# Spør brukeren om nødvendig informasjon
OperatingSystem = input('\nWhich operating system are you connecting from? (W or L) ->')
SerialPortNumber = input('\nEnter serial port number ->')
Hostname = input('\nEnter desired hostname ->')
MGMTPort = input('\nEnter management port number ->')
IPAddress = input('\nEnter desired IP address AND subnet mask->')
SSHUsername = input('\nEnter SSH Username ->')
SSHSecret = input('\nEnter SSH Password ->')
EnableSecret = input('\nEnter Enable Password ->')

# Lager portnavn basert på operativsystem
SerialPortNameLinux = '/dev/ttyS' + SerialPortNumber
SerialPortNameWindows = 'COM' + SerialPortNumber

# Lager kommandoer som skal sendes til enheten via seriell
HostnameString = 'hostname ' + Hostname + '\r\n'
MGMTPortString = 'int ' + MGMTPort + '\r\n'
IPAddressString = 'ip address ' + IPAddress + '\r\n'
SSHCredentials = 'username ' + SSHUsername + ' privilege 15 secret ' + SSHSecret + '\r\n'
EnableSecretString = 'enable secret ' + EnableSecret + '\r\n'

# Hovedfunksjonen som setter opp enheten via seriell tilkobling
def main():
	print("\nInitializing serial connection")

	# Sjekker hvilket operativsystem som brukes og åpner riktig port
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
	
	# Skriver ut navnet på porten
	print(console.name)

	# Hvis porten ikke er åpen, avslutt programmet
	if not console.isOpen():
		sys.exit()
	console.write("enable\r\n".encode())
	console.write("conf t\r\n".encode())
	console.write(HostnameString.encode())
	console.write(MGMTPortString.encode())
	console.write(IPAddressString.encode())
	console.write("no shutdown\r\n".encode())
	time.sleep(2)
	console.write("exit\r\n".encode())
	# Setter domenenavn og genererer RSA-nøkler for SSH
	console.write("ip domain name mynetwork.local\r\n".encode())
	console.write("crypto key generate rsa modulus 1024\r\n".encode())

	# Leser eventuell respons fra enheten (f.eks. RSA-dialog)
	input_data = console.read(console.inWaiting())
	print(input_data)
	time.sleep(3)

	# Setter SSH-bruker og aktiverer SSH-tilgang på VTY-linjer
	console.write(SSHCredentials.encode())
	console.write("line vty 0 15\r\n".encode())
	console.write("transport input ssh\r\n".encode())
	console.write("login local\r\n".encode())
	console.write("exec-timeout 60 0\r\n".encode())
	console.write("exit\r\n".encode())

	# Setter Enable-passord
	console.write(EnableSecretString.encode())

	# Leser eventuell respons fra enheten
	input_data = console.read(console.inWaiting())
	print(input_data)

# Starter hovedfunksjonen hvis scriptet kjøres direkte
if __name__ == "__main__":
	main()