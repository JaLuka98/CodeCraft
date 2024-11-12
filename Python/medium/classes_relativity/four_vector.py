from abc import ABC, abstractmethod
import math

class FourVector(ABC):
    """
    Abstract Base Class for Four-Vectors.
    """
    def __init__(self, px=0.0, py=0.0, pz=0.0, E=0.0):
        # Private attributes
        self._px = px
        self._py = py
        self._pz = pz
        self._E = E
        self._calculate_derived_quantities()
    
    def _calculate_derived_quantities(self):
        """Calculate derived quantities based on core attributes."""
        self._pt = math.sqrt(self._px**2 + self._py**2)
        self._phi = math.atan2(self._py, self._px)
        p = math.sqrt(self._px**2 + self._py**2 + self._pz**2)
        if p != abs(self._pz):
            self._eta = 0.5 * math.log((p + self._pz) / (p - self._pz))
        else:
            self._eta = float('inf') if self._pz >= 0 else -float('inf')
        self._M = math.sqrt(max(self._E**2 - p**2, 0))
    
    # Read-only properties for core attributes
    @property
    def px(self):
        return self._px
    
    @property
    def py(self):
        return self._py
    
    @property
    def pz(self):
        return self._pz
    
    @property
    def E(self):
        return self._E
    
    # Read-only properties for derived quantities
    @property
    def pt(self):
        return self._pt
    
    @property
    def eta(self):
        return self._eta
    
    @property
    def phi(self):
        return self._phi
    
    @property
    def M(self):
        return self._M
    
    @abstractmethod
    def set_vector(self, *args, **kwargs):
        """
        Abstract method to set the vector components.
        Must be implemented by subclasses.
        """
        pass
    
    def __add__(self, other):
        if not isinstance(other, FourVector):
            return NotImplemented
        return PxPyPzEFourVector(
            self.px + other.px,
            self.py + other.py,
            self.pz + other.pz,
            self.E + other.E
        )
    
    def __sub__(self, other):
        if not isinstance(other, FourVector):
            return NotImplemented
        return PxPyPzEFourVector(
            self.px - other.px,
            self.py - other.py,
            self.pz - other.pz,
            self.E - other.E
        )
    
    def __repr__(self):
        return (f"{self.__class__.__name__}(px={self.px}, py={self.py}, "
                f"pz={self.pz}, E={self.E}, pt={self.pt}, "
                f"eta={self.eta}, phi={self.phi}, M={self.M})")

class PxPyPzEFourVector(FourVector):
    """
    FourVector initialized with (px, py, pz, E).
    Immutable class.
    """
    def __init__(self, px, py, pz, E):
        super().__init__(px, py, pz, E)
    
    def set_vector(self, px, py, pz, E):
        """
        Since the class is immutable, attempting to set vector components raises an error.
        """
        raise AttributeError("FourVector instances are immutable and cannot be modified.")

class PxPyPzMFourVector(FourVector):
    """
    FourVector initialized with (px, py, pz, M).
    Immutable class.
    """
    def __init__(self, px, py, pz, M):
        E = math.sqrt(px**2 + py**2 + pz**2 + M**2)
        super().__init__(px, py, pz, E)
    
    def set_vector(self, px, py, pz, M):
        """
        Since the class is immutable, attempting to set vector components raises an error.
        """
        raise AttributeError("FourVector instances are immutable and cannot be modified.")


class PtEtaPhiEFourVector(FourVector):
    """
    FourVector initialized with (pt, eta, phi, E).
    Immutable class.
    """
    def __init__(self, pt, eta, phi, E):
        px = pt * math.cos(phi)
        py = pt * math.sin(phi)
        pz = pt * math.sinh(eta)
        super().__init__(px, py, pz, E)
    
    def set_vector(self, pt, eta, phi, E):
        """
        Since the class is immutable, attempting to set vector components raises an error.
        """
        raise AttributeError("FourVector instances are immutable and cannot be modified.")


class PtEtaPhiMFourVector(FourVector):
    """
    FourVector initialized with (pt, eta, phi, M).
    Immutable class.
    """
    def __init__(self, pt, eta, phi, M):
        px = pt * math.cos(phi)
        py = pt * math.sin(phi)
        pz = pt * math.sinh(eta)
        E = math.sqrt(px**2 + py**2 + pz**2 + M**2)
        super().__init__(px, py, pz, E)
    
    def set_vector(self, pt, eta, phi, M):
        """
        Since the class is immutable, attempting to set vector components raises an error.
        """
        raise AttributeError("FourVector instances are immutable and cannot be modified.")
    
# Example Usage
if __name__ == '__main__':
    # Also try to create abstract class will raise error
    # Using PxPyPzEFourVector
    p1 = PxPyPzEFourVector(px=1, py=2, pz=3, E=4)
    print(f"PxPyPzE: {p1}")
    # Attempting to modify (should raise AttributeError)
    try:
        p1.px = 2
    except AttributeError as e:
        print(f"Error: {e}")
    
    # Using PxPyPzMFourVector
    p2 = PxPyPzMFourVector(px=1, py=2, pz=3, M=0.9)
    print(f"PxPyPzM: {p2}")
    # Attempting to set M (should raise AttributeError)
    try:
        p2.set_vector(px=2, py=4, pz=6, M=1.0)
    except AttributeError as e:
        print(f"Error: {e}")
    
    # Using PtEtaPhiEFourVector
    p3 = PtEtaPhiEFourVector(pt=1, eta=0.5, phi=0.1, E=4)
    print(f"PtEtaPhiE: {p3}")
    # Attempting to modify (should raise AttributeError)
    try:
        p3.px = 2
    except AttributeError as e:
        print(f"Error: {e}")
    
    # Using PtEtaPhiMFourVector
    p4 = PtEtaPhiMFourVector(pt=1, eta=0.5, phi=0.1, M=0.9)
    print(f"PtEtaPhiM: {p4}")
    
    # Adding two four-vectors
    p5 = p1 + p2
    print(f"p1 + p2: {p5}")
    
    # Subtracting two four-vectors
    p6 = p1 - p2
    print(f"p1 - p2: {p6}")
