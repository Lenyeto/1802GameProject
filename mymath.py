import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)
    
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x + other, self.y + other)
        
        raise TypeError(" cannot add Vector2 and " + str(type(other)) + ' ')
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x - other, self.y - other)
        
        raise TypeError(" cannot subtract Vector2 and " + str(type(other)) + ' ')
    
    def __mul__(self, other):
        # if 'other' is a Vector2, perform dot product
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
        
        raise TypeError(" cannot multiply Vector2 and " + str(type(other)) + ' ')
    
    def __div__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x / other, self.y / other)
        
        raise TypeError(" cannot divide Vector2 and " + str(type(other)) + ' ')
    
    def __radd__(self, other):
        return self + other
    
    def __rsub__(self, other):
        raise TypeError(" cannot subtract Vector2 from " + str(type(other)) + ' ')
    
    def __rmul__(self, other):
        return self * other
    
    def __rdiv__(self, other):
        raise TypeError(" cannot divide Vector2 into " + str(type(other)) + ' ')
    
    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
        else:
            raise TypeError(" cannot add Vector2 and " + str(type(other)) + ' ')
            
        return self
    
    def __isub__(self, other):
        if isinstance(other, Vector2):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
        else:
            raise TypeError(" cannot subtract Vector2 and " + str(type(other)) + ' ')
        
        return self
    
    def __imul__(self, other):
        # if 'other' is a Vector2, raise TypeError since it returns a scalar, not Vector2
        if isinstance(other, Vector2):
            raise TypeError(" cannot multiply and assign since this will return a scalar value")
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
        else:
            raise TypeError(" cannot multiply Vector2 and " + str(type(other)) + ' ')
        
        return self
    
    def __idiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
        else:
            raise TypeError(" cannot divide Vector2 and " + str(type(other)) + ' ')
        
        return self
    
    def copy(self):
        return Vector2(self.x, self.y)
    
    def length(self):
        return self.length2() ** 0.5
    
    def length2(self):
        return self.x ** 2 + self.y ** 2
    
    def normalize(self):
        tmplen = self.length2()
        if tmplen != 0:
            tmplen **= 0.5
            self.x /= tmplen
            self.y /= tmplen
    
    def getAngle(self):
        angle = math.degrees(math.atan2(self.y, self.x))
        if angle < 0:
            angle = 360 + angle
        
        return angle
    
    def getNormalized(self):
        v = self.copy()
        v.normalize();
        return v
    
    def getPerpendicular(self):
        return Vector2(-self.y, self.x)
    
    def rotate(self, angle, origin=None):
        if not isinstance(origin, Vector2):
            origin = Vector2()
        
        ca = math.cos(math.radians(angle))
        sa = -math.sin(math.radians(angle))
        
        old_x = self.x
        self.x = origin.x + self.x * ca + self.y * sa
        self.y = origin.y + old_x * -sa + self.y * ca