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
"""Relabel Fermionic or Qubit Operator from activate space reduction."""
from typing import Tuple, Union
from openfermion.ops.operators import QubitOperator, FermionOperator
from openfermion.utils import count_qubits


def _relabel_single_pauli(term: Tuple, active_space_start: int,
                          initial_num_qubits: int) -> Tuple:
    """
    Relabel single Pauli term.

    Auxiliar function to qubitoperator_relabel

    Args:
        operator (QubitOperator): Operator to relabel.
        active_space_start (int): spatial orbit from where the active space
            starts.
        initial_num_qubits (int): number of qubits before reduced active space.
    Returns:
        relabel_operator: Operator with reduced labels.

    Notes:
        If operator acts on a qubit from frozen orbital, this operator is
        removed.
    """
    if term[0] == ():
        return term

    qubits, paulis = zip(*term[0])

    new_label = str()
    for qbt, pau in zip(qubits, paulis):
        if qbt in list(range(2 * active_space_start)):
            return None
        else:
            qbt = qbt - 2 * (active_space_start)
            new_label += pau + str(qbt) + str(' ')

    return (new_label, term[1])


def _relabel_single_fermion(term: Tuple, active_space_start: int,
                            initial_num_qubits: int) -> Tuple:
    """
    Relabel single Pauli operator.

    Auxiliar function to qubitoperator_relabel

    Args:
        operator (QubitOperator): Operator to relabel.
        active_space_start (int): spatial orbit from where the active space
            starts.
        initial_num_qubits (int): number of qubits before reduced active space.
    Returns:
        relabel_operator: Operator with reduced labels.

    Notes:
        If operator acts on a qubit from frozen orbital, this operator is
        removed.
    """
    if term[0] == ():  # Do nothing if operator is empty
        return term

    fermion, action = zip(*term[0])

    new_label = []
    for fer, act in zip(fermion, action):
        if fer in list(range(2 * active_space_start)):
            return None
        else:
            new_q = (fer - 2 * active_space_start, act)
            new_label.append(new_q)  # append tuple of new label

    return (new_label, term[1])


def operator_relabel(operator: Union[QubitOperator, FermionOperator],
                     active_space_start: Union[int, float]
                     ) -> Union[QubitOperator, FermionOperator]:
    """
    Relabel operator with reduced activate space.

    Args:
        operator (QubitOperator): Operator to relabel.
        active_space_start (int): spatial orbit from where the active space
            starts.
    Returns:
        relabel_operator (QubitOperator): Operator with reduced labels.

    Notes:
        If operator acts on a qubit from frozen orbital, this operator is
        removed.
    Raises:
        TypeError: if activate space is not an integer or float.
        ValueError: if starting space and qubits do not match.
        TypeError: if operator is not a QubitOperator.
    """
    if isinstance(active_space_start, (int, float)):
        active_space_start = int(active_space_start)
    else:
        raise TypeError('Active space start must be integer or float.')

    initial_num_qubits = count_qubits(operator)

    if 2 * active_space_start > initial_num_qubits:
        raise ValueError('Starting active space larger than initial qubits.')

    if isinstance(operator, QubitOperator):
        relabeled_op = QubitOperator()
        for term in operator.terms.items():

            term = _relabel_single_pauli(term, active_space_start,
                                         initial_num_qubits)
            if term is None:
                continue
            else:
                relabeled_op += QubitOperator(term[0], term[1])

        return relabeled_op

    elif isinstance(operator, FermionOperator):
        relabeled_op = FermionOperator()
        for term in operator.terms.items():

            term = _relabel_single_fermion(term, active_space_start,
                                           initial_num_qubits)

            if term is None:
                continue
            else:
                relabeled_op += FermionOperator(term[0], term[1])
        return relabeled_op

    else:
        raise TypeError('Operator must be a Qubit or Fermion type.')
