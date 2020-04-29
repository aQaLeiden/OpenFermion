# -*- coding: utf-8 -*-

import unittest
from openfermion import (QubitOperator,
                         FermionOperator)
from openfermion.utils._relabel_operators import (relabel_fermi_operator,
                                                  relabel_pauli_operator)


class Relabel_Operator_Test(unittest.TestCase):
    
    def test_types(self):
        '''
        Test if Raise error work
        '''
        qubit_op = QubitOperator('X2', 1.)
        fermi_op = FermionOperator((2,1), 1.)
        
        with self.assertRaises(TypeError):
            relabel_fermi_operator(0.,0.)
        with self.assertRaises(TypeError):
            relabel_pauli_operator(0.,0.)
        with self.assertRaises(ValueError):
            relabel_fermi_operator(fermi_op,2)
        with self.assertRaises(ValueError):
            relabel_pauli_operator(qubit_op,2)
    
    def test_relabel_fermi(self):
        '''
        Test relabel_fermi_operator
        '''
        fermi_op_1 = FermionOperator((4,1), 1.)
        fermi_op_2 = FermionOperator((2,1), 1.)
        
        self.assertTrue(relabel_fermi_operator(fermi_op_1,1) == fermi_op_2)
        self.assertTrue(relabel_fermi_operator(fermi_op_1,0) == fermi_op_1)# Identity test
        
    def test_relabel_pauli(self):
        '''
        Test relabel_pauli_operator
        '''
        qubit_op_1 = QubitOperator('X4', 1.)
        qubit_op_2 = QubitOperator('X2', 1.)
        
        self.assertTrue(relabel_pauli_operator(qubit_op_1,1) == qubit_op_2)
        self.assertTrue(relabel_pauli_operator(qubit_op_1,0) == qubit_op_1)# Identity test
        
if __name__ == '__main__':
    unittest.main()