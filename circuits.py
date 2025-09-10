class Resistor:
    def __init__(self, resistance_ohms):
        self.resistance = resistance_ohms

    def power_dissipation(self, voltage, current):
        return voltage * current

    def __add__(self, other):
        if isinstance(other, Resistor):
            return Resistor(self.resistance + other.resistance)
        raise ValueError("Can only add another Resistor")
    
    def __mul__(self, other):
        if isinstance(other, Resistor):
            return Resistor((self.resistance * other.resistance) / (self.resistance + other.resistance))
        elif isinstance(other, (int, float)):
            return Resistor(self.resistance * other)
        raise ValueError("Can only multiply with another Resistor")
    
    def __repr__(self):
        return f"Resistor({self.resistance} Ω)"

def quick_parrel(r1, r2):
    return (r1 * r2) / (r1 + r2)
    