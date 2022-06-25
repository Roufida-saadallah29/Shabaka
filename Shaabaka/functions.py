from telnetlib import Telnet
from time import sleep



def set_ip_for_pc(port,ip,def_getaway="192.168.1.1"):
    try:
        connection = Telnet(host='localhost',port=int(port))
    except:
        return "Error occured when establishing connection with device"
    connection.write(b"ip "+ip.encode()+b" 255.255.255.0  "+def_getaway.encode()+b"\r")
    sleep(1)
    connection.write(b"wr\r")
    res = connection.read_very_eager().decode()
    if("MAC" in res):
        return "Ip address already taken"
    if("Invalid address" in res):
        return "Invalid ip address"
    if("Invalid gateway address" in res):
        return "Invalid gateway address"
    if("Checking for duplicate address..."in res):
        connection.close()
        return  ip+" was assigned successfully"
    return "Something went wrong, please try again"

def set_ip_for_router_interface(port,ip,interface):
    try:
        connection = Telnet(host="localhost",port=int(port))
    except:
        return "error when establishing connection with device"
    connection.write(b"configure terminal\rinterface "+interface.encode()+b"\rip address "+ip.encode()+b" 255.255.255.0\r")
    sleep(1)
    if("^" in "".join(connection.read_very_eager().decode().split("\n")[-3])):
        connection.close()
        return "Something went wrong try again"
    connection.write(b"no shutdown\rend\rwr\r")
    connection.close()
    return ip+" was assigned to interface: "+interface

def set_dhcp(router):
    port_r = "5010"
    ip_int = "192.168.1.1" 
    port_1 = "5006"
    port_2 = "5002"
    if(router=='5011'):
        port_r = "5011"
        ip_int = "192.168.2.1"
        port_1 = "5005"
        port_2 = "5007"    
    set_ip_for_router_interface(port_r,ip_int,"f0")
    connection = Telnet(host="localhost",port=port_r)
    if(router == '5010' ):
        connection.write(b"configure terminal\rservice dhcp\rip dhcp excluded-address 192.168.1.1\rip dhcp excluded-address 192.168.1.254\rip dhcp pool r1\rnetwork 192.168.1.0 255.255.255.0\rdefault-router 192.168.1.1\rend\rwr\r")
    else:
        connection.write(b"configure terminal\rservice dhcp\rip dhcp excluded-address 192.168.2.1\rip dhcp excluded-address 192.168.2.254\rip dhcp pool r2\rnetwork 192.168.2.0 255.255.255.0\rdefault-router 192.168.2.1\rend\rwr\r")
    sleep(5)
    connection.close()
    connection1 = Telnet("localhost",port=port_1)
    connection2 = Telnet("localhost",port=port_2)
    connection1.write(b"ip dhcp\r")
    sleep(5)
    connection2.write(b"ip dhcp\r")
    connection1.write(b"wr\r")
    sleep(5)
    connection2.write(b"wr\r")
    connection1.close()
    connection2.close()
    return 0

def remove_dhcp(router):
    if(router == '5010'):
        connection = Telnet("localhost",5010)
    else:
        connection = Telnet("localhost",5011)
    connection.write(b"configure terminal\rno service dhcp\rend\rwr\r")
    connection.close()
    return 0

def set_rip():
    connection = Telnet("localhost",5010)
    connection.write(b"configure terminal\rrouter rip\rversion 2\rnetwork 192.168.1.0\rnetwork 192.168.3.0\rno auto-summary\rend\rwr\r")
    connection.close()
    connection = Telnet("localhost",5012)
    connection.write(b"configure terminal\rrouter rip\rversion 2\rnetwork 192.168.3.0\rno auto-summary\rend\rwr\r")
    connection.close()
    connection = Telnet("localhost",5011)
    connection.write(b"configure terminal\rrouter rip\rversion 2\rnetwork 192.168.2.0\rnetwork 192.168.3.0\rno auto-summary\rend\rwr\r")
    connection.close()
    return 0

def remove_rip():
    connection = Telnet("localhost",5010)
    connection.write(b"configure terminal\rno router rip\rend\rwr\r")
    connection.close()
    connection = Telnet("localhost",5012)
    connection.write(b"configure terminal\rno router rip\rend\rwr\r")
    connection.close()
    connection = Telnet("localhost",5011)
    connection.write(b"configure terminal\rno router rip\rend\rwr\r")
    connection.close()
    return 0

def set_ospf():
    set_ip_for_router_interface("5012","192.168.3.1","s0")
    set_ip_for_router_interface("5012","192.168.3.2","s1")
    connection = Telnet("localhost",5012)
    connection.write(b"configure terminal\rrouter ospf 1\rnetwork 192.168.3.0 0.0.0.255 area 0\rend\rwr\r")
    connection.close()
    set_ip_for_router_interface("5010","192.168.3.3","s0")
    connection = Telnet("localhost",5010)
    connection.write(b"configure terminal\rrouter ospf 1\rnetwork 192.168.3.0 0.0.0.255 area 0\rnetwork 192.168.1.0 0.0.0.255 area 0\rend\rwr\r")
    connection.close()
    set_ip_for_router_interface("5011","192.168.3.4","s0")
    connection = Telnet("localhost",5011)
    connection.write(b"configure terminal\rrouter ospf 1\rnetwork 192.168.3.0 0.0.0.255 area 0\rnetwork 192.168.2.0 0.0.0.255 area 0\rend\rwr\r")
    connection.close()

    return 0

def remove_ospf():
    connection = Telnet("localhost",5010)
    connection.write(b"configure terminal\rno router ospf 1\rend\rwr\r")
    connection.close()
    connection = Telnet("localhost",5011)
    connection.write(b"configure terminal\rno router ospf 1\rend\rwr\r")
    connection.close()
    connection = Telnet("localhost",5012)
    connection.write(b"configure terminal\rno router ospf 1\rend\rwr\r")
    connection.close()
    return 0

def get_routing_table_pc(port):
    connection = Telnet(host="localhost",port=port)
    connection.write(b"show ip\r")
    sleep(1)
    res = []
    for i in connection.read_very_eager().decode().split("\n\r")[-2::-1]:
        if 'show' in i:
            break
        res.append(i)
    return "\n".join(res)

def get_routing_table_router(port):
    connection = Telnet(host="localhost",port=port)
    connection.write(b"show ip interface brief\r")
    sleep(2)
    res = connection.read_very_eager().decode().split("\n")[-6:-1:]
    res.insert(1,"-------------------------------------------------------------------------------------")
    return "\n".join(res)
    
def get_ospf_neighboor(port):
    connection = Telnet(host="localhost",port=port)
    connection.write(b"show ip ospf neighbor\r")
    sleep(1)
    res = []
    for i in connection.read_very_eager().decode().split("\n")[-4:-1:]:
        if (not ('#' in i) and not ('*' in i) and not ('%' in i) and len(i) > 10):
            res.append(i)
    return "\n".join(res)

def get_rip_database(port):
    connection = Telnet(host="localhost",port=port)
    connection.write(b"show ip rip database\r")
    sleep(2)
    res = []
    for i in connection.read_very_eager().decode().split("\n")[-2:-20:-1]:
        if (('#' in i)):
            break
        res.insert(0,i)        
    return "\n".join(res)
    
def ping(port,address):
    connection = Telnet("localhost",port=port)
    connection.write(b"ping "+address.encode()+b"\r")
    res = []
    for i in range(0,5):
        sleep(1)
        res.append(connection.read_very_eager().decode().strip())
    return "\n".join(res)

def get_dhcp_binding(port):
    connection = Telnet('localhost',port=port)
    connection.write(b"show ip dhcp binding\r")
    sleep(1)
    res = []
    tmp =  connection.read_very_eager().decode().split('\r\n')[-2::-1]
    for i in tmp:
        if('#' in i):
            break
        res.insert(0,i)
    return '\n'.join(res)