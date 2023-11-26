import requests
from .helpers import SnapdAdapter

class SnapdClient():
    def __init__(self):
        self.session = requests.Session()
        self.session.mount("http://snapd/", SnapdAdapter())
    
    def snap_system_info(self):
        response = self.session.get("http://snapd/v2/system-info")
        return response.json()

    def refresh(self):
        response = self.session.post("http://snapd/v2/snaps", json={"action": "refresh"})
        return response.json()

    def revert(self, snap):
        response = self.session.post("http://snapd/v2/snaps/"+snap, json={"action": "revert"})
        return response.json()

    def list(self):
        response = self.session.get("http://snapd/v2/snaps")
        return response.json()
    
    def validation_sets(self):
        response = self.session.get("http://snapd/v2/validation-sets")
        return response.json()
    
    def enforce_validation(self, sequence):
        data = {"action": "refresh", "validation-sets": ["SgO2EXiK2bwgtciB1mNjMYM6zcljwXZt/baydogar-1={}".format(sequence)]}
        response = self.session.post("http://snapd/v2/snaps", json=data)
        return response.json()

    def forget_validation(self):
        response = self.session.post("http://snapd/v2/validation-sets/SgO2EXiK2bwgtciB1mNjMYM6zcljwXZt/baydogar-1", json={"action" : "forget"})
        return response.json()