# holds all necessary variables to share across scripts

class AppState():
    def __init__(self):
        self.hr = 0
        self.power = 0
        self.speed = 0
        self.target_adress = None
        self.device_name = None
        self.is_connected = False


shared_state = AppState()
