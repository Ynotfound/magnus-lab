class DimensionSystem:
    def parse(self, expr):
        """Simplified dimensional analysis for physics formulas"""
        # Map of known symbols to dimensional exponents [mass, length, time]
        dimensions = {
            'F': [1, 1, -2],    # Force: kg·m/s²
            'P': [1, -1, -2],   # Pressure: kg/(m·s²)
            'v': [0, 1, -1],     # Velocity: m/s
            'm': [1, 0, 0],     # Mass: kg
            'a': [0, 1, -2],    # Acceleration: m/s²
            'E': [1, 2, -2],    # Energy: kg·m²/s²
            'c': [0, 1, -1],    # Speed: m/s
            'h': [1, 2, -1],    # Planck's constant: kg·m²/s
            'G': [-1, 3, -2],   # Gravitational constant: m³/(kg·s²)
            # Add more as needed
        }

        # Basic expression parser (simplified)
        result = [0, 0, 0]  # [mass, length, time]

        # Handle multiplication/division
        tokens = expr.replace('*', ' * ').replace('/', ' / ').split()
        sign = 1

        for token in tokens:
            if token == '*':
                continue
            elif token == '/':
                sign = -1
                continue

            # Handle exponents
            if '^' in token:
                base, exp = token.split('^')
                exp = int(exp)
            else:
                base = token
                exp = 1

            # Get dimensions of base symbol
            if base in dimensions:
                dim = dimensions[base]
                for i in range(3):
                    result[i] += sign * exp * dim[i]

            sign = 1  # Reset sign after division

        return result

def equivalent(dim1, dim2):
    """Check if two dimensional representations are equivalent"""
    return dim1 == dim2