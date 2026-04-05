import re

class DimensionSystem:
    def parse(self, expr):
        """Physics dimensional analysis using dictionary-based representation"""
        # Physical dimension mapping to standard SI base quantities
        dimensions = {
            # Base quantities
            'kg': {'mass': 1, 'length': 0, 'time': 0},
            'm': {'mass': 0, 'length': 1, 'time': 0},
            's': {'mass': 0, 'length': 0, 'time': 1},

            # Common physics symbols
            'F': {'mass': 1, 'length': 1, 'time': -2},  # Force
            'P': {'mass': 1, 'length': -1, 'time': -2}, # Pressure
            'v': {'mass': 0, 'length': 1, 'time': -1},  # Velocity
            'a': {'mass': 0, 'length': 1, 'time': -2},  # Acceleration
            'E': {'mass': 1, 'length': 2, 'time': -2},  # Energy
            'c': {'mass': 0, 'length': 1, 'time': -1},  # Speed of light
            'h': {'mass': 1, 'length': 2, 'time': -1},  # Planck's constant
            'G': {'mass': -1, 'length': 3, 'time': -2}, # Gravitational constant
            'f': {'mass': 0, 'length': 0, 'time': -1},  # Frequency
            'r': {'mass': 0, 'length': 1, 'time': 0},  # Radius/distance
            'd': {'mass': 0, 'length': 1, 'time': 0},  # Distance
            'm1': {'mass': 1, 'length': 0, 'time': 0}, # Mass 1
            'm2': {'mass': 1, 'length': 0, 'time': 0}, # Mass 2
            'mass': {'mass': 1, 'length': 0, 'time': 0}, # Generic mass
        }

        # Initialize dimensional representation
        dim = {'mass': 0, 'length': 0, 'time': 0}
        current_sign = 1  # 1 for multiplication, -1 for division

        # Tokenize the expression
        tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\d+|\*\*|\*|/|=', expr)

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
                # Reset for right-hand side
                dim = {'mass': 0, 'length': 0, 'time': 0}
                current_sign = 1
                i += 1
                continue

            # Handle exponents
            exponent = 1
            if i + 1 < len(tokens) and tokens[i+1] == '**':
                try:
                    exponent = int(tokens[i+2])
                    i += 2  # Skip ** and exponent
                except (ValueError, IndexError):
                    pass

            # Find matching dimension (exact or partial match)
            var_dim = {'mass': 0, 'length': 0, 'time': 0}
            for key, value in dimensions.items():
                if key in token or token in key:
                    var_dim = value
                    break

            # Apply to total dimension
            for quantity in ['mass', 'length', 'time']:
                dim[quantity] += current_sign * exponent * var_dim[quantity]


            current_sign = 1  # Reset sign after processing term
            i += 1

        return dim

def equivalent(dim1, dim2):
    """Deep comparison of dimensional dictionaries"""
    return (
        dim1['mass'] == dim2['mass'] and
        dim1['length'] == dim2['length'] and
        dim1['time'] == dim2['time']
    )