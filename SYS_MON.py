from pathlib import Path
import subprocess
import psutil
class SystemResource:
    def __init__(self, name, status):
        self.name = name
        self.status = status
    def check_health(self):
        pass
    def get_metrics(self):
        pass
class ServiceManager(SystemResource):
    def start(self):
        pass
    def stop(self):
        pass
    def is_active(self):
        active = subprocess.run(["systemctl", "is-active", self.name], capture_output=True, text=True)
        return active.stdout.strip() == "active"
    def check_health(self):
        if self.is_active():
            return F'[Service] {self.name}: Running '
        else:
            return f'[Service] {self.name}: Down '
class StorageDrive(SystemResource):
    def __init__(self, name, status, mount_point):
        super().__init__(name, status)
        self.mount_point = mount_point  
    def calculate_used_percentage(self): 
        try:
            usg = psutil.disk_usage(self.mount_point)
        except FileNotFoundError:
            return -1
        return usg.used / usg.total * 100
        
    def warn_if_full(self):
        usage = self.calculate_used_percentage()
        if usage  == -1:
            return (F"Disk not found: {self.mount_point}")
        elif usage > 90:
            return "Drive is over 90% full"
        else:
            return "OK"
    def check_health(self):
        disk_info = self.warn_if_full()
        return F'[DRIVE] {self.name} {self.mount_point} {disk_info}' 
class NetworkInterface(SystemResource):
    def __init__(self, name, status):
        super().__init__(name, status)
    def ping_gateway(self):
        pass
    def get_ip_address(self):
        addr_check = psutil.net_if_addrs()
        if self.name in addr_check:
            return addr_check[self.name][0].address
        else:
            return "Interface not found"
    def check_health(self):
        addr = self.get_ip_address()
        return F'[NETWORK] {self.name} IP:{addr}'             
class AuditorEngine:
    def __init__(self):
        self.components = [ ]
    def add_resource(self, resource):
        self.components.append(resource)
    def run_audit(self):
        for item in self.components:
            print (item.check_health())

my_drive = StorageDrive("root","Active", "/")
my_serv = ServiceManager("firewalld", "Active")
my_drive2 = StorageDrive("root", "Active", "/boot/efi")
my_serv2 = ServiceManager("update", "Active" )
my_drive3 = StorageDrive("root", "Active", "/boost/efi")
my_interf = NetworkInterface("lo", "Net")
my_interf2 = NetworkInterface("lo1", "Net")

engine = AuditorEngine()
engine.add_resource(my_drive)
engine.add_resource(my_serv)
engine.add_resource(my_drive2)
engine.add_resource(my_serv2)
engine.add_resource(my_drive3)
engine.add_resource(my_interf)
engine.add_resource(my_interf2)
engine.run_audit()
