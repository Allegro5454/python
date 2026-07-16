from pathlib import Path
import subprocess
import psutil
import json
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
    def to_dict(self):
        return {"type":"ServiceManager",
                "name":self.name,
                "status":self.is_active()
                }
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
    def to_dict(self):
        return {"type":"StorageDrive",
                "name":self.name,
                "status":self.status,
                "usage":self.calculate_used_percentage()
                }
    
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
    def to_dict(self):
        return {"type":"NetworkInterface",
                "name":self.name,
                "address":self.get_ip_address(),
                }
    
class AuditorEngine:
    def __init__(self):
        self.components = [ ]
    def add_resource(self, resource):
        self.components.append( resource )
    def run_audit(self):
        log = [ ]
        for item in self.components:
            print (item.check_health())
            log.append(item.to_dict())
        with open('audit_log.json', 'w') as log_file:
            json.dump(log, log_file, indent=4)
engine = AuditorEngine()

with open('config.json', 'r') as file:
    config_data = json.load(file)
    for elem in config_data:
        if elem["type"] == "ServiceManager":
            engine.add_resource( ServiceManager(elem["name"], elem["status"]) )
        elif elem["type"] == "StorageDrive":
            engine.add_resource( StorageDrive( elem["name"], elem["status"], elem["mount_point"]))
        elif elem["type"] == "NetworkInterface":
            engine.add_resource( NetworkInterface(elem["name"], elem["status"]))
 
engine.run_audit()
