from fractions import Fraction, gcd
from operator import add, sub, mul

Fraction.__repr__ = Fraction.__str__

class Matrix:
    def __init__(self, m):
        # make sure it is at least rectangular
        assert all([len(m[i]) == len(m[i + 1]) for i in range(len(m) - 1)])
        self.m = [[m[i][j] for j in range(len(m[0]))] for i in range(len(m))]
        self.h = len(self.m)
        self.w = len(self.m[0])
        self.shape = (self.h, self.w)
    
    def __str__(self):
        m = "\n".join([", ".join([str(item) + "\t" for item in row]) for row in self])
        return "Matrix(\n" + m + "\n)"
    
    def __repr__(self):
        return str(self)
    
    def __len__(self):
        return len(self.m)
    
    def __getitem__(self, idx):
        return self.m[idx]
    
    def __setitem__(self, idx, value):
        self.m[idx] = value
    
    def __add__(self, other):
        assert self.shape == other.shape, "Matrix dimension mismatch {} and {}".format(self.shape, other.shape)
        for i in range(self.h):
            for j in range(self.w):
                self[i][j] += other[i][j]
        return self
    
    def __sub__(self, other):
        assert self.shape == other.shape, "Matrix dimension mismatch {} and {}".format(self.shape, other.shape)
        for i in range(self.h):
            for j in range(self.w):
                self[i][j] -= other[i][j]
        return self
                
    def __mul__(self, other):
        for i in range(self.h):
            for j in range(self.w):
                self[i][j] *= other[i][j]        
        return self
    
    def copy(self):
        return Matrix([[self[i][j] for j in range(len(self[0]))] for i in range(len(self))])
    
    def matmul(self, other):
        assert self.w == len(other), "Matrices dimension mismatch {} and {}".format(self.shape, other.shape)
        zip_b = list(zip(*other))
        return Matrix([[sum(i * j for i, j in zip(row_a, col_b)) 
                 for col_b in zip_b] for row_a in self])
    
    def transpose(self):
        return Matrix(list(map(list, zip(*self.m))))
        
    def dot(self, vector):
        assert self.h == len(vector), "Matrix and vector dimension mismatch {} and {}".format(self.shape, len(vector))
        return [Matrix.scalar(row, vector) for row in self]
    
    def remove_col(self, idx):
        m = self.copy()
        for i in range(len(m)):
            m[i].pop(idx)
        return Matrix(m)
    
    def remove_row(self, idx):
        m = self.copy()
        m.m.pop(idx)
        return Matrix(m)
    
    def submatrix(self, rows, cols):
        return Matrix([[self[row][col] for col in cols] for row in rows])
    
    def augment(self):
        m = self.copy()
        for i, row in enumerate(m):
            row.extend([int(i == j) for j in range(len(row))])
        return Matrix(m)
    
    def reduced_row_echelon(self, right=None):
        assert self.w == self.h
        m = self.copy()
        
        lead = 0
        rowCount = len(m)
        columnCount = len(m[0])
        for r in range(rowCount):
            if lead >= columnCount:
                return m, right
            i = r
            while m[i][lead] == 0:
                i += 1
                if i == rowCount:
                    i = r
                    lead += 1
                    if columnCount == lead:
                        return m, right
            m[i], m[r] = m[r],m[i]
            lv = m[r][lead]
            m[r] = [ mrx / lv for mrx in m[r]]
            if right is not None:
                right[i], right[r] = right[r], right[i]
                right[r] = [ mrx / lv for mrx in right[r]]
            for i in range(rowCount):
                if i != r:
                    lv = m[i][lead]
                    m[i] = [iv - lv * rv for rv,iv in zip(m[r],m[i])]
                    if right is not None:
                        right[i] = [iv - lv * rv for rv,iv in zip(right[r], right[i])]
            lead += 1
        return m, right
    
    def inverse(self):
        """
        If the matrix is invertible, finds the inverse of a matrix by Gauss-Jordan elimination
        """
        # check it is square
        assert self.w == self.h
        
        m = self.copy()
        I_m = Matrix.identity_like(m)
        m, inv = self.reduced_row_echelon(right=I_m)
        return inv
        
    def canonical(self):
        """
        Returns the canonical for of the matrix as if
        it is a transition matrix of an absorbing markov chain
        | Q | R |
         ___ ___
        | 0 | I |
        """
        # init mat
        p = self.copy()
        # get fractions
        for i in range(len(p)):
            rsum = sum(p[i])
            # check if terminal
            if rsum == 0:
                # if terminal, the only possible step is itself
                p[i][i] = 1
                continue
            for j in range(len(p[i])):
                fraction = Fraction(p[i][j], rsum)
                p[i][j] = fraction
        return Matrix(p)
    
    @staticmethod
    def identity(n):
        return Matrix([[int(i == j) for j in range(n)] for i in range(n)])
    
    @staticmethod
    def identity_like(m):
        n = min([len(m), len(m[0])])
        return Matrix.identity(n)
    
    @staticmethod
    def scalar(row, column):
        return sum(map(mul, row, column))


class NudeFraction:
    def __init__(self, num, den):
        self.numerator = num
        self.denominator = den
    
    def __str__(self):
        return str(self.numerator) + "/" + str(self.denominator)
    
    def __repr__(self):
        return str(self)


def get_Q(m):
    q = m.copy()
    non_absorb = []
    for i in range(len(m)):
        # is state `i` absorbing?:
        if not (sum(m[i]) == 1 and m[i][i] == 1):
            non_absorb.append(i)
    return m.submatrix(non_absorb, non_absorb)


def get_R(m):
    q = m.copy()
    absorb, non_absorb = [], []
    for i in range(len(m)):
        # is state `i` absorbing?:
        if sum(m[i]) == 1 and m[i][i] == 1:
            absorb.append(i)
        else:
            non_absorb.append(i)
    return m.submatrix(non_absorb, absorb)


def get_N(m):
    Q = get_Q(m)
    I = Matrix.identity_like(Q)
    N = I - Q
    return N.inverse()


def get_B(m):
    N = get_N(m)
    R = get_R(m)
    return N.matmul(R)


def lcm(fractions):
    m = 1
    for i in range(len(fractions)):
        a = fractions[i].denominator
        m = m * a // gcd(m, a)
    return [NudeFraction(m // item.denominator * item.numerator, m) for item in fractions]


def solution(m):
    mat = Matrix(m)
    mat = mat.canonical()
    
    # if s1 is terminal, return
    if sum(mat[0]) == 1 and mat[0][0] == 1:
        return [1, 1]
    
    B = get_B(mat)
    
    result = []
    # we always start from s1,
    # so we take just the first row of B
    probs = lcm(B[0])
    numerators = [item.numerator for item in probs]
    numerators.append(probs[0].denominator)
    return numerators

def test():
    tests = [
        [[1, 0], [0, 0]],
        [[0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[1, 1, 1, 1, 1,], [0, 0, 0, 0, 0,], [1, 1, 1, 1, 1,], [0, 0, 0, 0, 0,], [1, 1, 1, 1, 1,]],
        [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    ]
    for test in tests:
        print solution(test)
    return

if __name__ == "__main__":
    test()