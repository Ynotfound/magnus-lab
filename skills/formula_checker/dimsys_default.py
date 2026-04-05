import re
class DimensionSystem:
    def parse(self, expr):
        """Comprehensive dimensional analysis for physics formulas"""
        # Map of known symbols to dimensional exponents [mass, length, time]
        dimensions = {
            # Base physical quantities
            'm': [1, 0, 0],      # mass
            'kg': [1, 0, 0],    # mass
            'length': [0, 1, 0],
            'L': [0, 1, 0],
            'r': [0, 1, 0],     # radius
            'd': [0, 1, 0],     # distance
            'x': [0, 1, 0],     # position
            'time': [0, 0, 1],
            't': [0, 0, 1],

            # Derived quantities
            'F': [1, 1, -2],    # Force: kg·m/s²
            'P': [1, -1, -2],   # Pressure: kg/(m·s²)
            'v': [0, 1, -1],     # Velocity: m/s
            'a': [0, 1, -2],    # Acceleration: m/s²
            'E': [1, 2, -2],    # Energy: kg·m²/s²
            'c': [0, 1, -1],    # Speed of light: m/s
            'h': [1, 2, -1],    # Planck's constant: kg·m²/s
            'G': [-1, 3, -2],   # Gravitational constant: m³/(kg·s²)
            'f': [0, 0, -1],     # Frequency: 1/s
            'ω': [0, 0, -1],    # Angular frequency
            'k': [0, -1, 0],    # Wave number
            'A': [0, 2, 0],     # Area
            'V': [0, 3, 0],     # Volume

            # Variable patterns (partial matches)
            'm1': [1, 0, 0],
            'm2': [1, 0, 0],
            'mass': [1, 0, 0],
            'frequency': [0, 0, -1],
            'pressure': [1, -1, -2],
        }

        # Extract variable names from expression (simplified)
        tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\*\*|\*|/|\^|=', expr)

        # Track dimensional exponents [mass, length, time]
        result = [0, 0, 0]
        current_sign = 1  # 1 for multiplication, -1 for division

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token == '*':
                i += 1
                continue
            elif token == '/':
                current_sign = -1
                i += 1
                continue
            elif token == '=':
                # Reset for right side
                result = [0, 0, 0]
                current_sign = 1
                i += 1
                continue

            # Handle variable with possible exponent
            var = token
            exponent = 1

            # Check for exponent notation
            if i + 2 < len(tokens) and tokens[i+1] == '**':
                try:
                    exponent = int(tokens[i+2])
                    i += 2  # Skip ** and exponent
                except (ValueError, IndexError):
                    pass

            # Determine dimension from variable
            dim = [0, 0, 0]
            for key in dimensions:
                if key in var or var in key:  # Partial match
                    dim = dimensions[key]
                    break

            # Apply dimension with sign and exponent
            for j in range(3):
                result[j] += current_sign * exponent * dim[j]

            current_sign = 1  # Reset sign after processing a term
            i += 1

        return result

def equivalent(dim1, dim2):
    """Check if two dimensional representations are equivalent"""
    return dim1 == dim2