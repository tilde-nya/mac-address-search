import details # Formatted as list of tuples ("IP", "Switch Type")
sw = details.switches
username = details.username
password = details.password
import telnetlib

# def findmac(mac):
#     con = telnetlib.Telnet()
#     for i in switches:
#         con.open(i, port=23)
#         con.

#         con.close()


def convert(mac, format):
    """
    Converts MAC Address to certain format

    formats:
    - "HP"
    - "COLON"
    - "DASH"
    """

    mac = "".join(ch for ch in mac if ch.isalnum())

    if (len(mac) != 12):
        print("error")
        return

    if (format.upper() == "HP"):
        mac = mac[0:4] + "-" + mac[4:8] + "-" + mac[8:12]
    elif (format.upper() == "COLON"):
        mac = mac[0:2] + ":" + mac[2:4] + ":" + mac[4:6] + ":" + mac[6:8] + ":" + mac[8:10] + ":" + mac[10:12]
    elif (format.upper() == "DASH"):
        mac = mac[0:2] + "-" + mac[2:4] + "-" + mac[4:6] + "-" + mac[6:8] + "-" + mac[8:10] + "-" + mac[10:12]

    return mac.upper()


import telnetlib


tn = telnetlib.Telnet(host=sw[0][0], port=23)

tn.read_until(b"User:", timeout=2)
tn.write((username + "\r\n").encode("utf-8"))
tn.read_until(b"Password:", timeout=2)
tn.write((password + "\r\n").encode("utf-8"))
tn.read_until(b">", timeout=5)
tn.write(b"enable\r\n")
tn.read_until(b"#", timeout=5)

tn.write(("show mac address-table address " + convert("00-be-43-d8-3a-a0", "COLON") + "\r\b").encode("utf-8"))
print(tn.read_until(b"Total MAC Addresses for this criterion: ", timeout=3).decode())

print(tn.read_eager().decode())
tn.write(b"logout\r\n")
tn.close()