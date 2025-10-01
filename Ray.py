class Ray:
    """Ray with origin, direction, and optional time."""
    def __init__(self, orig, dir, time=0.0):
        self.orig = orig
        self.dir = dir
        self.tm = time

    def origin(self):
        return self.orig

    def direction(self):
        return self.dir

    def time(self):
        return self.tm

    def at(self, t):
        return self.orig + (t * self.dir)
