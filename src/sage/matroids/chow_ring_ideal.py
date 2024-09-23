r"""
Chow ring ideals of matroids

AUTHORS:

- Shriya M
"""

from sage.rings.polynomial.multi_polynomial_ideal import MPolynomialIdeal
from sage.matroids.utilities import cmp_elements_key
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.polynomial.multi_polynomial_sequence import PolynomialSequence
from sage.misc.abstract_method import abstract_method
from itertools import combinations
from functools import reduce

class ChowRingIdeal(MPolynomialIdeal):
    @abstract_method
    def matroid(self):
        r"""
        Return the matroid of the given Chow ring ideal.

        EXAMPLES::
            
            sage: ch = matroids.Uniform(3,6).chow_ring(QQ, False)
            sage: ch.defining_ideal().matroid()
            U(3, 6): Matroid of rank 3 on 6 elements with circuit-closures
            {3: {{0, 1, 2, 3, 4, 5}}}
        """
        M = self._matroid
        return M
    
    def flats_generator(self):
        r"""
        Return the variables of every corresponding flat/groundset element
        of the matroid.

        EXAMPLES::

            sage: ch = matroids.catalog.Fano().chow_ring(QQ, False)
            sage: ch.defining_ideal().flats_generator()
            {frozenset({'a'}): Aa, frozenset({'b'}): Ab, frozenset({'c'}): Ac,
            frozenset({'d'}): Ad, frozenset({'e'}): Ae, frozenset({'f'}): Af,
            frozenset({'g'}): Ag, frozenset({'b', 'a', 'f'}): Aabf,
            frozenset({'c', 'e', 'a'}): Aace, frozenset({'d', 'g', 'a'}): Aadg,
            frozenset({'c', 'b', 'd'}): Abcd, frozenset({'b', 'g', 'e'}): Abeg,
            frozenset({'c', 'g', 'f'}): Acfg, frozenset({'d', 'e', 'f'}): Adef}
        """
        return dict(self._flats_generator)
    

class ChowRingIdeal_nonaug(ChowRingIdeal): 
    r"""
    The Chow ring ideal of a matroid `M`.

    The *Chow ring ideal* for a matroid `M` is defined as the ideal
        `(Q_M + L_M)` of the polynomial ring:
    
    ..MATH::

        R[x_{F_1}, \ldots, x_{F_k}]

    where

    - `F_1, \ldots, F_k` are the non-empty flats of `M`,
    - `Q_M` is the ideal generated by all `x_{F_i} x_{F_j}` where
      `F_i` and `F_j` are incomparable elements in the lattice of
       flats, and
    - `L_M` is the ideal generated by all linear forms

      .. MATH::

          \sum_{i_1 \in F} x_F - \sum_{i_2 \in F} x_F

      for all `i_1 \neq i_2 \in E`.
    
    INPUT:

    - `M` -- a matroid
    - `R` -- a commutative ring

    REFERENCES:

    - [ANR2023]_

    EXAMPLES:

    Chow ring ideal of uniform matroid of rank 3 on 6 elements::

        sage: ch = matroids.Uniform(3,6).chow_ring(QQ, False)
        sage: ch.defining_ideal()
        Chow ring ideal of U(3, 6): Matroid of rank 3 on 6 elements with
        circuit-closures {3: {{0, 1, 2, 3, 4, 5}}}
        sage: ch = matroids.catalog.Fano().chow_ring(QQ, False)
        sage: ch.defining_ideal()
        Chow ring ideal of Fano: Binary matroid of rank 3 on 7 elements,
        type (3, 0)
    """
    def __init__(self, M, R):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: I = matroids.catalog.Fano().chow_ring(QQ, False).defining_ideal()
            sage: TestSuite(I).run(skip="_test_category")
        """
        self._matroid = M
        flats = [X for i in range(1, self._matroid.rank())
                 for X in self._matroid.flats(i)]
        names = ['A{}'.format(''.join(str(x) for x in sorted(F, key=cmp_elements_key))) for F in flats]
        try:
            poly_ring = PolynomialRing(R, names) #self.ring
        except ValueError: # variables are not proper names
            poly_ring = PolynomialRing(R, 'A', len(flats))
        gens = poly_ring.gens()
        self._flats_generator = dict(zip(flats, gens))
        MPolynomialIdeal.__init__(self, poly_ring, self._gens_constructor(poly_ring))

    def _gens_constructor(self, poly_ring):
        r"""
        Returns the generators of `self`. Takes in the
        ring of Chow ring ideal as input.
        
        EXAMPLES::

            sage: ch = matroids.catalog.NonFano().chow_ring(QQ, False)
            sage: ch.defining_ideal()._gens_constructor(ch.defining_ideal().ring())
            [Aa*Ab, Aa*Ac, Aa*Ad, Aa*Ae, Aa*Af, Aa*Ag, Aa*Abcd, Aa*Abeg,
            Aa*Acfg, Aa*Ade, Aa*Adf, Aa*Aef, Ab*Ac, Ab*Ad, Ab*Ae, Ab*Af, Ab*Ag,
            Ab*Aace, Ab*Aadg, Ab*Acfg, Ab*Ade, Ab*Adf, Ab*Aef, Ac*Ad, Ac*Ae,
            Ac*Af, Ac*Ag, Ac*Aabf, Ac*Aadg, Ac*Abeg, Ac*Ade, Ac*Adf, Ac*Aef,
            Ad*Ae, Ad*Af, Ad*Ag, Ad*Aabf, Ad*Aace, Ad*Abeg, Ad*Acfg, Ad*Aef,
            Ae*Af, Ae*Ag, Ae*Aabf, Ae*Aadg, Ae*Abcd, Ae*Acfg, Ae*Adf, Af*Ag,
            Af*Aace, Af*Aadg, Af*Abcd, Af*Abeg, Af*Ade, Ag*Aabf, Ag*Aace,
            Ag*Abcd, Ag*Ade, Ag*Adf, Ag*Aef, Aabf*Aace, Aabf*Aadg, Aabf*Abcd,
            Aabf*Abeg, Aabf*Acfg, Aabf*Ade, Aabf*Adf, Aabf*Aef, Aace*Aadg,
            Aace*Abcd, Aace*Abeg, Aace*Acfg, Aace*Ade, Aace*Adf, Aace*Aef,
            Aadg*Abcd, Aadg*Abeg, Aadg*Acfg, Aadg*Ade, Aadg*Adf, Aadg*Aef,
            Abcd*Abeg, Abcd*Acfg, Abcd*Ade, Abcd*Adf, Abcd*Aef, Abeg*Acfg,
            Abeg*Ade, Abeg*Adf, Abeg*Aef, Acfg*Ade, Acfg*Adf, Acfg*Aef,
            Ade*Adf, Ade*Aef, Adf*Aef,
            -Ab + Ae - Aabf + Aace - Abcd + Ade + Aef,
            -Ac + Ae - Abcd + Abeg - Acfg + Ade + Aef,
            Ae - Ag + Aace - Aadg - Acfg + Ade + Aef,
            -Ad + Ae + Aace - Aadg - Abcd + Abeg - Adf + Aef,
            -Aa + Ae - Aabf - Aadg + Abeg + Ade + Aef,
            Ae - Af - Aabf + Aace + Abeg - Acfg + Ade - Adf,
            Ab - Ac + Aabf - Aace + Abeg - Acfg,
            Ab - Ag + Aabf - Aadg + Abcd - Acfg,
            Ab - Ad + Aabf - Aadg + Abeg - Ade - Adf,
            -Aa + Ab - Aace - Aadg + Abcd + Abeg,
            Ab - Af + Abcd + Abeg - Acfg - Adf - Aef,
            Ac - Ag + Aace - Aadg + Abcd - Abeg,
            Ac - Ad + Aace - Aadg + Acfg - Ade - Adf,
            -Aa + Ac - Aabf - Aadg + Abcd + Acfg,
            Ac - Af - Aabf + Aace + Abcd - Adf - Aef,
            -Ad + Ag - Abcd + Abeg + Acfg - Ade - Adf,
            -Aa + Ag - Aabf - Aace + Abeg + Acfg,
            -Af + Ag - Aabf + Aadg + Abeg - Adf - Aef,
            -Aa + Ad - Aabf - Aace + Abcd + Ade + Adf,
            Ad - Af - Aabf + Aadg + Abcd - Acfg + Ade - Aef,
            Aa - Af + Aace + Aadg - Acfg - Adf - Aef]
        """
        E = list(self._matroid.groundset())
        flats = list(self._flats_generator.keys())
        flats_containing = {x: [] for x in E}
        for i,F in enumerate(flats):
            for x in F:
                flats_containing[x].append(i)
        gens = poly_ring.gens()
        Q = [gens[i] * gens[i+j+1] for i,F in enumerate(flats)
            for j,G in enumerate(flats[i+1:]) if not (F < G or G < F)] #Quadratic Generators
        L = [sum(gens[i] for i in flats_containing[x])
            - sum(gens[i] for i in flats_containing[y])
            for j,x in enumerate(E) for y in E[j+1:]] #Linear Generators
        return Q + L

    def _repr_(self):
        r"""
        EXAMPLES::

            sage: ch = matroids.catalog.Fano().chow_ring(QQ, False)
            sage: ch.defining_ideal()
            Chow ring ideal of Fano: Binary matroid of rank 3 on 7 elements, type (3, 0)
        """
        return "Chow ring ideal of {}- non augmented".format(self._matroid)

    def groebner_basis(self, algorithm='constructed'): #can you reduce it? - consider every antichain of size 2, and chains?
        r"""
        Returns the Groebner basis of `self`.

        EXAMPLES::

            sage: from sage.matroids.basis_matroid import BasisMatroid

            sage: ch = BasisMatroid(groundset='abc', bases=['ab', 'ac'])).chow_ring(QQ, False)
            sage: ch.defining_ideal().groebner_basis(algorithm='')
            [Aa, Abc]
            sage: ch.defining_ideal().groebner_basis(algorithm='').is_groebner()
            True
        
        Another example would be the Groebner basis of the Chow ring ideal of
        the Graphic matroid of CycleGraph(3)::

            sage: from sage.matroids.graphic_matroid import GraphicMatroid

            sage: ch = GraphicMatroid(graphs.CycleGraph(3)).chow_ring(QQ, False)
            sage: ch.defining_ideal().groebner_basis(algorithm='')
            [A0, A1, A2, A0*A1, A0*A2, A1*A2, A0*A1*A2]
            sage: ch.defining_ideal().groebner_basis(algorithm='').is_groebner()
            True
        """
        if algorithm == '':
            flats = list(self._flats_generator)
            gb = list()
            R = self.ring() 
            if frozenset() in flats:
                flats.remove(frozenset()) #Non-empty proper flats needed
                
            ranks = {F:self._matroid.rank(F) for F in flats}

            flats_gen = self._flats_generator
            subsets = []
            # Generate all subsets of flats using combinations
            for r in range(len(flats) + 1):  # r is the size of the subset
                subsets.extend(list(subset) for subset in combinations(flats, r))

            for subset in subsets:
                flag = True
                sorted_list = sorted(subset, key=len)
                for i in range (len(sorted_list)): #Checking whether the subset is a chain
                    if (i != 0) & (len(sorted_list[i]) == len(sorted_list[i-1])):
                        flag = False
                        break

                if not flag: 
                    term = R.one()
                    for x in subset:
                        term *= flats_gen[x]
                    gb.append(term)
                
                else:
                    if subset == []:
                        for F in flats:
                            term = R.zero()
                            for G in flats:
                                if G >= F:
                                    term += flats_gen[G]
                            gb.append((term)**(ranks[F]))

                    else:
                        for j in range(len(subset)):
                            for k in range(j+1, len(subset)): #Checking if every element in the chain is maximal
                                if (sorted_list[j] != sorted_list[k]) & (sorted_list[j].issubset(sorted_list[k])):
                                    flag = False
                                    break

                        if flag:
                            for F in flats:
                                if F > reduce(lambda a, b: a.union(b), sorted_list): 
                                    term = R.one()
                                    for x in subset:
                                        term *= flats_gen[x]
                                    term1 = R.zero()
                                    for G in flats:
                                        if G >= F:
                                            term1 += flats_gen[G]
                                    if term1 != R.zero():
                                        gb.append(term*(term1**(ranks[F] - ranks[sorted_list[len(subset) - 1]])))
                
            g_basis = PolynomialSequence(R, [gb])
            return g_basis
        
        elif algorithm == 'constructed': #*args **kwds
            super().groebner_basis()

    
class AugmentedChowRingIdeal_fy(ChowRingIdeal):
    r"""
    The augmented Chow ring ideal of matroid `M` over ring `R` in
    Feitchner-Yuzvinsky presentation.

    The augmented Chow ring ideal in the Feitchner-Yuzvinsky presentation
    for a matroid `M` is defined as the ideal
        `(I_M + J_M)` of the following polynomial ring:

    ..MATH::

        R[y_{e_1}, \ldots, y_{e_n}, x_{F_1}, \ldots, x_{F_k}]

    as

    - `F_1, \ldots, F_k` are the non-empty proper flats of `M`,
    - `e_1 \ldots, e_n` are `n` elements of groundset of `M`,
    - `J_M` is the ideal generated by all quadratic forms `x_{F_i} x_{F_j}`
       where `F_i` and `F_j` are incomparable elements in the lattice of
       flats, and `y_{i} x_F` for every `i \in E` and `i \notin F`, and
    -  `I_M` is the ideal generated by all linear forms

    ..MATH::

        y_i - \sum_{i \notin F} x_F 

    for all `i \in E`.
    
    REFERENCES:

    - [MM2022]_

    INPUT:


    - `M` -- a matroid
    - `R` -- a commutative ring

    EXAMPLES::

    Augmented Chow ring ideal of Wheel matroid of rank 3::

        sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'fy')
        sage: ch.defining_ideal()
        Augmented Chow ring ideal of Wheel(3): Regular matroid of rank 3 on 
        6 elements with 16 bases of Feitchner-Yuzvinsky presentation
    """
    def __init__(self, M, R):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: I = matroids.Wheel(3).chow_ring(QQ, True, 'fy').defining_ideal()
            sage: TestSuite(I).run(skip="_test_category")
        """
        self._matroid = M
        self._flats = [X for i in range(1, self._matroid.rank())
                for X in self._matroid.flats(i)]
        E = list(self._matroid.groundset())
        self._flats_generator = dict()
        try:
            names_groundset = ['A{}'.format(''.join(str(x))) for x in E]
            names_flats = ['B{}'.format(''.join(str(x) for x in sorted(F, key=cmp_elements_key))) for F in self._flats]
            poly_ring = PolynomialRing(R, names_groundset + names_flats) #self.ring()
        except ValueError: #variables are not proper names
            poly_ring = PolynomialRing(R, 'A', len(E) + len(self._flats))
        for i,x in enumerate(E):
            self._flats_generator[x] = poly_ring.gens()[i]
        for i,F in enumerate(self._flats):
            self._flats_generator[F] = poly_ring.gens()[len(E) + i]
        MPolynomialIdeal.__init__(self, poly_ring, self._gens_constructor(poly_ring))
        
    
    def _gens_constructor(self, poly_ring):
        r"""
        Return the generators of `self`. Takes in the ring of
        that augmented Chow ring ideal as input.

        EXAMPLES::

            sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'fy')
            sage: ch.defining_ideal()._gens_constructor(ch.defining_ideal().ring())
            [B0^2, B0*B1, B0*B2, B0*B3, B0*B4, B0*B5, B0*B124, B0*B15, B0*B23,
            B0*B345, B0*B1, B1^2, B1*B2, B1*B3, B1*B4, B1*B5, B1*B025, B1*B04,
            B1*B23, B1*B345, B0*B2, B1*B2, B2^2, B2*B3, B2*B4, B2*B5, B2*B013,
            B2*B04, B2*B15, B2*B345, B0*B3, B1*B3, B2*B3, B3^2, B3*B4, B3*B5,
            B3*B025, B3*B04, B3*B124, B3*B15, B0*B4, B1*B4, B2*B4, B3*B4, B4^2,
            B4*B5, B4*B013, B4*B025, B4*B15, B4*B23, B0*B5, B1*B5, B2*B5,
            B3*B5, B4*B5, B5^2, B5*B013, B5*B04, B5*B124, B5*B23, B2*B013,
            B4*B013, B5*B013, B013^2, B013*B025, B013*B04, B013*B124, B013*B15,
            B013*B23, B013*B345, B1*B025, B3*B025, B4*B025, B013*B025, B025^2,
            B025*B04, B025*B124, B025*B15, B025*B23, B025*B345, B1*B04, B2*B04,
            B3*B04, B5*B04, B013*B04, B025*B04, B04^2, B04*B124, B04*B15,
            B04*B23, B04*B345, B0*B124, B3*B124, B5*B124, B013*B124, B025*B124,
            B04*B124, B124^2, B124*B15, B124*B23, B124*B345, B0*B15, B2*B15,
            B3*B15, B4*B15, B013*B15, B025*B15, B04*B15, B124*B15, B15^2,
            B15*B23, B15*B345, B0*B23, B1*B23, B4*B23, B5*B23, B013*B23,
            B025*B23, B04*B23, B124*B23, B15*B23, B23^2, B23*B345, B0*B345,
            B1*B345, B2*B345, B013*B345, B025*B345, B04*B345, B124*B345,
            B15*B345, B23*B345, B345^2,
            A0 - B1 - B2 - B3 - B4 - B5 - B124 - B15 - B23 - B345,
            A1 - B0 - B2 - B3 - B4 - B5 - B025 - B04 - B23 - B345,
            A2 - B0 - B1 - B3 - B4 - B5 - B013 - B04 - B15 - B345,
            A3 - B0 - B1 - B2 - B4 - B5 - B025 - B04 - B124 - B15,
            A4 - B0 - B1 - B2 - B3 - B5 - B013 - B025 - B15 - B23,
            A5 - B0 - B1 - B2 - B3 - B4 - B013 - B04 - B124 - B23]

        """
        E = list(self._matroid.groundset())
        flats_containing = {x: [] for x in E}
        for F in self._flats:
            for x in F:
                flats_containing[x].append(F)

        Q = list()
        for F in self._flats:
            for G in self._flats:
                    if not (F < G or G < F):
                        Q.append(self._flats_generator[F] * self._flats_generator[G]) #Quadratic Generators
        L = list()
        for x in E:
            term = poly_ring.zero()
            for F in self._flats:
                if F not in flats_containing[x]:
                    term += self._flats_generator[F]
            L.append(self._flats_generator[x] - term) #Linear Generators
        return Q + L

    def _repr_(self):
        r"""
        EXAMPLES::

            sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'fy')
            sage: ch.defining_ideal()
            Augmented Chow ring ideal of Wheel(3): Regular matroid of rank 3 on 
            6 elements with 16 bases of Feitchner-Yuzvinsky presentation
        """
        return "Augmented Chow ring ideal of {} of Feitchner-Yuzvinsky presentation".format(self._matroid)
    
    def groebner_basis(self, algorithm='constructed'):
        r"""
        Returns the Groebner basis of `self`.

        EXAMPLES::

            sage: ch = matroids.Uniform(2,5).chow_ring(QQ, True, 'fy')
            sage: ch.defining_ideal().groebner_basis(algorithm='')
            Polynomial Sequence with 250 Polynomials in 10 Variables
            sage: ch.defining_ideal().groebner_basis(algorithm='').is_groebner()
            True
        """
        if algorithm == '':
            gb = []
            E = list(self._matroid.groundset())
            poly_ring = self.ring()
            for F in self._flats:
                for G in self._flats:
                    if not (F < G or G < F): #Non-nested flats
                            gb.append(self._flats_generator[F]*self._flats_generator[G])
                    for i in E:
                        term = poly_ring.zero()
                        term1 = poly_ring.zero()
                        for H in self._flats:
                            if i in H:
                                term += self._flats_generator[H]
                            if H > G:
                                term1 += self._flats_generator[H]
                        if term != poly_ring.zero():
                            gb.append(self._flats_generator[i] + term) #5.7
                        if term1 != poly_ring.zero():
                            gb.append(term1**(self._matroid.rank(G)) + 1) #5.6

                        if i in G: #if element in flat
                            if term1 != poly_ring.zero():
                                gb.append(self._flats_generator[i]*((term1)**self._matroid.rank(G)))
                
                        elif not i in G: #if element not in flat
                            gb.append(self._flats_generator[i]*self._flats_generator[F])
                        
                        elif G < F: #nested flats
                            gb.append(self._flats_generator[G]*term1**(self._matroid.rank(F)-self._matroid.rank(G)))

            g_basis = PolynomialSequence(poly_ring, [gb])
            return g_basis
        elif algorithm == 'constructed':
            super().groebner_basis()

class AugmentedChowRingIdeal_atom_free(ChowRingIdeal):
    r"""
    The augmented Chow ring ideal for a matroid `M` over ring `R` in the
    atom-free presentation.

    The augmented Chow ring ideal in the atom-free presentation for a matroid
    `M` is defined as the ideal
        `I_{af}(M)` of the polynomial ring:

    ..MATH::

        R[x_{F_1}, \ldots, x_{F_k}]

    as

        - `F_1, \ldots, F_k` are the non-empty proper flats of `M`,
        - `I_{af }M` is the ideal generated by all quadratic forms `x_{F_i} x_{F_j}`
           where `F_i` and `F_j` are incomparable elements in the lattice of
           flats, 
        
    ..MATH::

        x_F \sum_{i \in F'} x_{F'}

    for all `i \in E` and `i \notin F`, and

    ..MATH::

        \sum_{i \in F'} (x_{F'})^2

    for all `i \in E`.

    REFERENCES:

    - [MM2022]_

    INPUT:

    - ``M`` -- a matroid
    - ``R`` -- a commutative ring

    EXAMPLES:

    Augmented Chow ring ideal of Wheel matroid of rank 3::

        sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'atom-free')
        sage: ch.defining_ideal()
        Augmented Chow ring ideal of Wheel(3): Regular matroid of rank 3 on 
        6 elements with 16 bases of atom-free presentation
    """ 
    def __init__(self, M, R):
        r"""
        Initialize ``self``.

        EXAMPLES::

            sage: I = matroids.Wheel(3).chow_ring(QQ, True, 'atom-free').defining_ideal()
            sage: TestSuite(I).run(skip="_test_category")
        """
        self._matroid = M
        self._flats = [X for i in range(1, self._matroid.rank())
                 for X in self._matroid.flats(i)]
        
        E = list(self._matroid.groundset())
        flats_containing = {x: [] for x in E}
        for i,F in enumerate(self._flats):
            for x in F:
                flats_containing[x].append(i)

        names = ['A{}'.format(''.join(str(x) for x in sorted(F, key=cmp_elements_key))) for F in self._flats]

        try:
            poly_ring = PolynomialRing(R, names) #self.ring
        except ValueError: # variables are not proper names
            poly_ring = PolynomialRing(R, 'A', len(self._flats))
        gens = poly_ring.gens()
        self._flats_generator = dict()
        self._flats_generator = dict(zip(self._flats, gens))
        MPolynomialIdeal.__init__(self, poly_ring, self._gens_constructor(poly_ring))
        

    def _gens_constructor(self, poly_ring):
        r"""
        Return the generators of `self`. Takes in the ring of the augmented
        Chow ring ideal as input.

        EXAMPLES::

            sage: from sage.matroids.graphic_matroid import GraphicMatroid

            sage: M1 = GraphicMatroid(graphs.CycleGraph(3))
            sage: ch = M1.chow_ring(QQ, True, 'atom-free')
            sage: ch.defining_ideal()._gens_constructor(ch.defining_ideal().ring())
            [A0^2, A0^2, A1^2, A0*A1, A2^2, A0*A2, A0*A1, A0^2, A1^2, A0*A1,
            A2^2, A0*A2, A0*A2, A0^2, A1^2, A0*A1, A2^2, A0*A2, A0*A1, A0^2,
            A0*A1, A1^2, A2^2, A1*A2, A1^2, A0^2, A0*A1, A1^2, A2^2, A1*A2,
            A1*A2, A0^2, A0*A1, A1^2, A2^2, A1*A2, A0*A2, A0^2, A0*A2, A1^2,
            A1*A2, A2^2, A1*A2, A0^2, A0*A2, A1^2, A1*A2, A2^2, A2^2, A0^2,
            A0*A2, A1^2, A1*A2, A2^2]

        """
        E = list(self._matroid.groundset())
        Q = [] #Quadratic Generators
        flats_containing = {x: [] for x in E}
        for F in self._flats:
            for x in F:
                flats_containing[x].append(F)
        for F in self._flats:
            for G in self._flats:
                if not (G > F or F > G): #generators for every pair of non-nested flats
                        Q.append(self._flats_generator[F]*self._flats_generator[G])
                for x in E: #generators for every set of flats containing element
                    term = poly_ring.zero()
                    for H in flats_containing[x]:
                        term += self._flats_generator[H]
                    Q.append(term**2)

                    if F not in flats_containing[x]: #generators for every set of flats not containing element
                        term = poly_ring.zero()
                        for H in flats_containing[x]:
                            term += self._flats_generator[H]
                        Q.append(self._flats_generator[F]*term)

        return Q
            
    def _repr_(self):
        r"""
        EXAMPLE::

            sage: ch = matroids.Wheel(3).chow_ring(QQ, True, 'atom-free')
            sage: ch.defining_ideal()
            Augmented Chow ring ideal of Wheel(3): Regular matroid of rank 3 on 
            6 elements with 16 bases of atom-free presentation
        """
        return "Augmented Chow ring ideal of {} in the atom-free presentation".format(self._matroid)
    
    def groebner_basis(self, algorithm='constructed'):
        """
        Returns the Groebner basis of `self`.

        EXAMPLES::

            sage: from sage.matroids.graphic_matroid import GraphicMatroid

            sage: M1 = GraphicMatroid(graphs.CycleGraph(3))
            sage: ch = M1.chow_ring(QQ, True, 'atom-free')
            sage: ch.defining_ideal().groebner_basis(algorithm='')
            [A0^2, A0*A1, A0*A2, A0*A1, A1^2, A1*A2, A0*A2, A1*A2, A2^2]
            sage: ch.defining_ideal().groebner_basis(algorithm='').is_groebner()
            True
        """
        if algorithm == '':
            gb = []
            flats = [X for i in range(1, self._matroid.rank())
                    for X in self._matroid.flats(i)]
            poly_ring = self.ring()
            if frozenset() in flats: #Non empty proper flats
                flats.remove(frozenset())
            for F in flats:
                for G in flats:
                    if not (F > G or G > F): #Non nested flats
                        gb.append(self._flats_generator[F]*self._flats_generator[G])
                    elif F < G: #Nested flats
                        term = poly_ring.zero()
                        for H in flats:
                            if H < F:
                                term += self._flats_generator[H]
                        if term != poly_ring.zero():
                            gb.append(self._flats_generator[F]*(term**self._matroid.rank(G))*
                                (term**(self._matroid.rank(G)-self._matroid.rank(F))))

            g_basis = PolynomialSequence(poly_ring, [gb])
            return g_basis
        
        elif algorithm == 'constructed':
            super().groebner_basis()

            

        

