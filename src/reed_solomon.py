
import numpy as np

class ReedSolomon:
    def __init__(self, n, k):
        self.n = n  # Code word length
        self.k = k  # Message length
        self.t = (n - k) // 2  # Error correction capability

        # Generate Galois Field
        self.gf = self._generate_gf(n)
        
        # Generate generator polynomial
        self.g = self._generate_generator_polynomial()

    def _generate_gf(self, n):
        # Simplified Galois Field generation
        return list(range(n))

    def _generate_generator_polynomial(self):
        # Simplified generator polynomial
        return [1, 2, 3]  # This should be properly implemented

    def encode(self, message):
        if len(message) != self.k:
            raise ValueError("Message length must be equal to k")

        # Pad the message
        encoded = message + [0] * (self.n - self.k)

        # Perform polynomial division
        for i in range(self.k):
            coef = encoded[i]
            if coef != 0:
                for j in range(1, len(self.g)):
                    encoded[i + j] ^= self._gf_mul(self.g[j], coef)

        # Combine message and parity
        return message + encoded[self.k:]

    def decode(self, received):
        if len(received) != self.n:
            raise ValueError("Received word length must be equal to n")

        # Syndrome calculation
        syndromes = self._calculate_syndromes(received)

        if all(s == 0 for s in syndromes):
            return received[:self.k]  # No errors

        # Error locator polynomial
        error_locator = self._find_error_locator(syndromes)

        # Find error positions
        error_positions = self._find_errors(error_locator)

        # Correct errors
        corrected = self._correct_errors(received, error_positions, syndromes)

        return corrected[:self.k]

    def _calculate_syndromes(self, received):
        return [0] * (self.n - self.k)  # Simplified

    def _find_error_locator(self, syndromes):
        return [1, 0, 1]  # Simplified

    def _find_errors(self, error_locator):
        return [0, 2]  # Simplified

    def _correct_errors(self, received, error_positions, syndromes):
        corrected = received.copy()
        for pos in error_positions:
            corrected[pos] ^= 1  # Simplified error correction
        return corrected

    def _gf_mul(self, a, b):
        return (a + b) % len(self.gf)  # Simplified GF multiplication

# Example usage
if __name__ == "__main__":
    rs = ReedSolomon(15, 11)
    message = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    encoded = rs.encode(message)
    print("Encoded:", encoded)
    
    # Simulate an error
    received = encoded.copy()
    received[0] ^= 1
    
    decoded = rs.decode(received)
    print("Decoded:", decoded)
