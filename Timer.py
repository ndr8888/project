class Timer:
    def __init__(self, time_max):
        self.time_max = time_max
        self.time = 0

    def start(self):
        self.time = self.time_max

    def tick(self, time=1):
        self.time -= time
        if self.time < 0:
            self.time = 0

    def stop(self):
        self.time = 0
