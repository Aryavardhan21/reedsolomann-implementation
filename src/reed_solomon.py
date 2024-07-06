import numpy as np

class GF256:
    def __init__(self):
        self.exp = [0] * 256
        self.log = [0] * 256
        x = 1
        for i in range(1, 256):
            self.exp[i] = x
            self.log[x] = i
            x = self.xtime(x)

    def xtime(self, a):
        return ((a << 1) ^ 0x11B) & 0xFF if a & 0x80 else a << 1

    def add(self, a, b):
        return a ^ b

    def sub(self, a, b):
        return a ^ b

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp[(self.log[a] + self.log[b]) % 255]

    def div(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        if a == 0:
            return 0
        return self.exp[(self.log[a] - self.log[b]) % 255]

    def pow(self, a, n):
        if n == 0:
            return 1
        if a == 0:
            return 0
        return self.exp[(self.log[a] * n) % 255]

    def inverse(self, a):
        if a == 0:
            raise ZeroDivisionError("Division by zero")
        return self.exp[255 - self.log[a]]

class ReedSolomon:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.gf = GF256()

    def generate_generator_polynomial(self):
        g = [1]
        for i in range(self.n - self.k):
            g = self.poly_mul(g, [1, self.gf.pow(2, i)])
        return g

    def poly_mul(self, p1, p2):
        r = [0] * (len(p1) + len(p2) - 1)
        for i in range(len(p1)):
            for j in range(len(p2)):
                r[i+j] = self.gf.add(r[i+j], self.gf.mul(p1[i], p2[j]))
        return r

    def poly_div(self, dividend, divisor):
        quotient = [0] * len(dividend)
        remainder = dividend.copy()
        for i in range(len(dividend) - len(divisor) + 1):
            if remainder[i] != 0:
                factor = self.gf.div(remainder[i], divisor[0])
                quotient[i] = factor
                for j in range(len(divisor)):
                    remainder[i+j] = self.gf.sub(remainder[i+j], self.gf.mul(divisor[j], factor))
        return quotient, remainder

    def encode(self, message):
        if len(message) != self.k:
            raise ValueError("Message length must be equal to k")
        
        g = self.generate_generator_polynomial()
        padded_msg = message + [0] * (self.n - self.k)
        _, remainder = self.poly_div(padded_msg, g)
        return message + remainder[-(self.n - self.k):]

    def syndrome(self, received):
        s = [0] * (self.n - self.k)
        for i in range(self.n - self.k):
            for j in range(self.n):
                s[i] = self.gf.add(s[i], self.gf.mul(received[j], self.gf.pow(self.gf.pow(2, i), j)))
        return s

    def berlekamp_massey(self, s):
        C = [1]
        B = [1]
        L = 0
        m = 1
        N = len(s)
        for n in range(N):
            d = s[n]
            for i in range(1, L + 1):
                d = self.gf.add(d, self.gf.mul(C[i], s[n - i]))
            if d == 0:
                m += 1
            elif 2 * L <= n:
                T = C.copy()
                C = C + [0] * (len(B) - len(C))
                for i in range(len(B)):
                    C[i] = self.gf.sub(C[i], self.gf.mul(d, self.gf.mul(self.gf.inverse(B[0]), B[i])))
                L = n + 1 - L
                B = T
                m = 1
            else:
                C = C + [0] * (len(B) - len(C))
                for i in range(len(B)):
                    C[i] = self.gf.sub(C[i], self.gf.mul(d, self.gf.mul(self.gf.inverse(B[0]), B[i])))
                m += 1
        return C

    def find_roots(self, poly):
        roots = []
        for i in range(256):
            result = 0
            for j in range(len(poly)):
                result = self.gf.add(result, self.gf.mul(poly[j], self.gf.pow(i, j)))
            if result == 0:
                roots.append(i)
        return roots

    def correct_errors(self, received, error_locator):
        roots = self.find_roots(error_locator)
        if len(roots) != len(error_locator) - 1:
            return None  # Uncorrectable error

        syndromes = self.syndrome(received)
        error_evaluator = self.poly_mul(syndromes, error_locator)
        error_evaluator = error_evaluator[:len(error_locator)-1]

        X = [0] * len(roots)
        for i in range(len(roots)):
            X[i] = self.gf.pow(roots[i], 255 - 1)

        error_locations = [self.gf.log[255 - x] for x in X]
        
        E = [0] * self.n
        for i, location in enumerate(error_locations):
            Xi = X[i]
            err_eval = 0
            for j in range(len(error_evaluator)):
                err_eval = self.gf.add(self.gf.mul(Xi, err_eval), error_evaluator[j])
            
            err_loc_prime = 1
            for j in range(len(error_locations)):
                if j != i:
                    err_loc_prime = self.gf.mul(err_loc_prime, self.gf.sub(1, self.gf.mul(Xi, X[j])))
            
            magnitude = self.gf.div(err_eval, err_loc_prime)
            E[location] = magnitude

        corrected = [self.gf.sub(r, e) for r, e in zip(received, E)]
        return corrected

    def decode(self, received):
        if len(received) != self.n:
            raise ValueError("Received word length must be equal to n")

        syndromes = self.syndrome(received)
        if all(s == 0 for s in syndromes):
            return received[:self.k]  # No errors

        error_locator = self.berlekamp_massey(syndromes)
        corrected = self.correct_errors(received, error_locator)

        if corrected is None:
            raise ValueError("Uncorrectable error")

        return corrected[:self.k]

# Example usage
if __name__ == "__main__":
    n, k = 15, 11
    rs = ReedSolomon(n, k)

    # Original message
    message = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    print("Original message:", message)

    # Encode
    encoded = rs.encode(message)
    print("Encoded message:", encoded)

    # Simulate errors
    received = encoded.copy()
    received[0] ^= 1  # Flip a bit
    received[1] ^= 1  # Flip another bit
    print("Received (with errors):", received)

    # Decode
    try:
        decoded = rs.decode(received)
        print("Decoded message:", decoded)
        print("Successful decoding!" if decoded == message else "Decoding failed!")
    except ValueError as e:
        print("Decoding failed:", str(e))
