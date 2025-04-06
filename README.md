# Arbeidskrav4
## Forutsetninger
Denne guiden antar at du allerede har installert python3 og ansible.

Om din python installasjon ikke vet hva Serial er må du kanskje kjøre: sudo apt install python3-serial

Du bør ha rettigheter til å nå seriellportene: Kan gjøres (ikke anbefalt) med "sudo chmod 777 /dev/ttyS*"

Skriptene er testet med IP-planen som ligger under mappen Konfigurasjonsfiler.
Ansible konfigurasjonen antar at brukernavn og passordet er "cisco" over alt.

Som utgangspunkt skal innholdet i Hosts.txt inn i /etc/ansible/hosts på din linux installasjon. (Eller pek konfigurasjonsfilen mot en annen host lokasjon)

Jeg lagde en mappe under ~/ som het ansible hvor jeg satt ansible.cfg og de fire playbookene.

## Scripts for å sette opp SSH tilkobling
Legg python-skriptene der du måtte ønske, de peker ikke mot noen filer/filbaner.

***SwitchSetup.py***
1. Plugg inn seriell-kabelen fra din PC til switchen
2. Sørg for at det ikke er en åpen seriell kobling mot porten allerede, da får du ikke kjørt skriptet
3. Kjør SwitchSetup.py
4. Den spør etter operativsystem, seriellportnummer, hostname, om du vil ha trunk, om du trenger en accessport for management, VLAN for management, IP addresse for management, og SSH credentials
- Operativsystem (Den godtar l/L/linux/Linux og w/W/windows/Windows)
- Seriellportnummer (Bare skriv nummeret på porten. Hvis det er COM1 så skriv "1". Hvis det er /dev/ttyS5 så skriv "5"
- Hostname (Navnet du vil gi enheten)
- Trunk (Den godtar y/Y/yes/Yes og n/N/no/No)
  - Single eller range (den godtar single/Single og range/Range)
    - Single (Skriv portnummeret som enheten ville godtatt det. feks. "Gig1/0/1" eller "Fa0/1")
    - Range (Skriv port range som enheten ville godtatt det. feks. "Gig1/0/1-3" eller "Fa0/1-3")
- Management port (Vil du ha en access port i management VLAN vi oppretter?)
  - Hvis ja (Skriv portnummeret som enheten ville godtatt det. feks. "Gig1/0/1" eller "Fa0/1")
- Management VLAN (Skriv bare nummeret, jeg brukte "99" som management VLAN)
- IP Address and Subnet Mask (Skriv begge deler, feks. "192.168.0.254 255.255.255.0", det blir feil om man kun skriver IP.)
- SSH credentials (Jeg har brukt cisco som brukernavn og passord, og det må endres i config om du vil ha noe annet)
- Enable secret (Her også har jeg brukt cisco)
5. Når alt er fylt inn så kjører den skriptet og skriver ut det den har i loggen sin, gjerne se over om det er noen feil der
6. Dersom alt ser ok ut kan du fortsette til neste enhet

***RouterSetup.py***
1. Plugg inn seriell-kabelen fra din PC til ruteren
2. Sørg for at det ikke er en åpen seriell kobling mot porten allerede, da får du ikke kjørt skriptet
3. Kjør RouterSetup.py
4. Den spør etter operativsystem, seriellportnummer, hostname, hvilken port du skal ha management på, IP addresse for management, og SSH credentials
- Operativsystem (Den godtar l/L/linux/Linux og w/W/windows/Windows)
- Seriellportnummer (Bare skriv nummeret på porten. Hvis det er COM1 så skriv "1". Hvis det er /dev/ttyS5 så skriv "5"
- Hostname (Navnet du vil gi enheten)
- Management port (Skriv portnummeret som enheten ville godtatt det. feks. "Gig1/0/1" eller "Fa0/1")
- IP Address and Subnet Mask (Skriv begge deler, feks. "192.168.0.254 255.255.255.0", det blir feil om man kun skriver IP.)
- SSH credentials (Jeg har brukt cisco som brukernavn og passord, og det må endres i config om du vil ha noe annet)
- Enable secret (Her også har jeg brukt cisco)
5. Når alt er fylt inn så kjører den skriptet og skriver ut det den har i loggen sin, gjerne se over om det er noen feil der
6. Dersom alt ser ok ut kan du fortsette til neste enhet

## Konfigurasjonen jeg gjorde med skriptene
**Switch 1 | Cisco Catalyst 3650**
- *Hostname:* S1_STUD1
- *Trunk:* yes, range, Gig1/0/1-2
- *Management port:* yes, Gig1/0/3
- *VLAN:* 1
- *IP Address and subnet mask:* 192.168.0.254 255.255.255.0
- *SSH username:* cisco
- *SSH password:* cisco
- *Enable secret:* cisco

**Ruter 1 | Cisco 2901**
- *Hostname:* R1_STUD1
- *Management port:* Gig0/0/0
- *IP Address and subnet mask:* 192.168.0.2 255.255.255.0
- *SSH username:* cisco
- *SSH password:* cisco
- *Enable secret:* cisco

**Ruter 2 | Cisco 4221**
- *Hostname:* R2_STUD1
- *Management port:* Gig0/0
- *IP Address and subnet mask:* 192.168.0.3 255.255.255.0
- *SSH username:* cisco
- *SSH password:* cisco
- *Enable secret:* cisco

**Switch 2 | Cisco Catalyst 1000**
- *Hostname:* S2_STUD1
- *Trunk:* yes, range, Gig1/0/1-3
- *Management port:* no
- *VLAN:* 99
- *IP Address and subnet mask:* 10.10.99.101 255.255.255.0
- *SSH username:* cisco
- *SSH password:* cisco
- *Enable secret:* cisco

**Switch 3 | Cisco Catalyst 2960**
- *Hostname:* S3_STUD1
- *Trunk:* yes, range, Gig1/0/1-3
- *Management port:* no
- *VLAN:* 99
- *IP Address and subnet mask:* 10.10.99.102 255.255.255.0
- *SSH username:* cisco
- *SSH password:* cisco
- *Enable secret:* cisco

## Ansible konfigurasjon
Etter SSH er satt opp for alle enhetene skal du kunne kjøre ansible skriptene på enhetene (i rekkefølge, vi kommer ikke helt til switch 3 med en gang for eksempel).

For å kjøre playbooken skriver du bare: "ansible-playbook Router1.yml"

Switch 1 har ikke behov for ekstra konfigurasjon, så rekkefølgen er:
1. Router1.yml
2. Router2.yml
3. Switch2.yml
4. Switch3.yml

