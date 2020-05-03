#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Test relabel operators"""

import unittest
from openfermion import (QubitOperator,
                         FermionOperator)
from openfermion.utils._relabel_operators import (_relabel_single_pauli,
                                                  relabel_qubitoperator,
                                                  _relabel_single_fermi,
                                                  relabel_fermionoperator,)


class Relabel_FermionOperator_Test(unittest.TestCase):
    def test_function_raise(self):
        '''        Test function raises       '''
        fermi_op = FermionOperator('1^ 0', 1.)
        fermi_op1 = FermionOperator('3^ 2', 2.)

        with self.assertRaises(TypeError):
            relabel_fermionoperator(0.,0.)  
        with self.assertRaises(TypeError):
            relabel_fermionoperator(fermi_op,.5)   
        with self.assertRaises(ValueError):
            _relabel_single_fermi(fermi_op+fermi_op1,1,4)
        with self.assertRaises(ValueError):
            _relabel_single_fermi(fermi_op1,2,3)
            
    def test_fermioperator(self):
        '''     Test relabel_pauli_operator     '''
        op = FermionOperator('3^ 2^ 0', 1.0)
        op1 = FermionOperator('0^ 1', -1.0)
        op2 = FermionOperator('2^ 3', -1.0)
        op3 = FermionOperator('',0.5)

        
        self.assertTrue(relabel_fermionoperator(op2,1) == op1)
        self.assertTrue(relabel_fermionoperator(op,1) == FermionOperator()) #Return empty if frozen
        self.assertTrue(_relabel_single_fermi(op, 1, 4) == FermionOperator())
        self.assertTrue(relabel_fermionoperator(op,0) == op) #Do nothing
        self.assertTrue(relabel_fermionoperator(op3,3) == op3 ) #Empty operator doesn't change
        self.assertTrue(relabel_fermionoperator(op+op1+op2+op3,1) == op1+op3) #Combined
        
class Relabel_QubitOperator_Test(unittest.TestCase):
    def test_function_raise(self):
        '''        Test function raises       '''
        qubit_op = QubitOperator('X2', 1.)
        qubit_op1 = QubitOperator('Y4', 2.)

        with self.assertRaises(TypeError):
            relabel_qubitoperator(0.,0.)  
        with self.assertRaises(TypeError):
            relabel_qubitoperator(qubit_op,.5)   
        with self.assertRaises(ValueError):
            _relabel_single_pauli(qubit_op+qubit_op1,1,4)
        with self.assertRaises(ValueError):
            _relabel_single_pauli(qubit_op,2,3)
            
    def test_qubitoperator(self):
        '''     Test relabel_pauli_operator     '''
        op = QubitOperator('Z1 Z3 Z4', 1.0)
        op1 = QubitOperator('X0 Y1', -1.0)
        op2 = QubitOperator('X2 Y3', -1.0)
        op3 = QubitOperator('',0.5)

        
        self.assertTrue(relabel_qubitoperator(op2,1) == op1)
        self.assertTrue(relabel_qubitoperator(op,1) == QubitOperator())
        self.assertTrue(_relabel_single_pauli(op, 1, 4) == QubitOperator()) #Return empty if frozen
        self.assertTrue(relabel_qubitoperator(op,0) == op) #Do nothing
        self.assertTrue(relabel_qubitoperator(op3,3) == op3 ) #Empty operator doesn't change
        self.assertTrue(relabel_qubitoperator(op+op1+op2+op3,1) == op1+op3) #Combined
        