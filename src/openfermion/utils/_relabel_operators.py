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

"""Relabel FermionOperator and QubitOperator"""

from openfermion import QubitOperator, FermionOperator, count_qubits


def _relabel_single_pauli(operator, active_space_start, start_num_qbts):
    """
    Relabel single Pauli operator.

    Args:
        operator (QubitOperator): Operator to relabel.
        active_space_start (int): spatial orbit from where the active space
            starts.
        start_num_qbts (int): number of qubits before reducing active space.
    Returns:
        relabel_operator (QubitOperator): Operator with reduced labels.

    Notes:
        If operator acts on a qubit from frozen orbital, this operator is
        removed.

    Raises:
        TypeError: if operator is not a QubitOperator.
        ValueError: if number of terms in operator is more than 1.
    """
    if not isinstance(operator, QubitOperator):
        raise TypeError('Input must be a QubitOperator.')
    if len(operator.terms) > 1:
        raise ValueError('Input has more than 1 Pauli string.')
    if list(operator.terms.keys())[0] == ():
        return operator

    if 2 * active_space_start > start_num_qbts:
        raise ValueError('Starting active space larger than qubits.')

    qbts, paus = zip(*list(operator.terms.keys())[0])

    new_label = str()
    for q, p in zip(qbts, paus):
        if q in list(range(2 * active_space_start)):
            return QubitOperator()
        else:
            new_q = q - 2 * (active_space_start)
            new_label += p + str(new_q) + str(' ')

    return QubitOperator(new_label, list(operator.terms.values())[0])


def relabel_qubitoperator(qubitop, active_space_start):
    """
    Relabel qubitop with reduced activate space.

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
        TypeError: if operator is not a QubitOperator.
        ValueError: if number of terms in operator is more than 1.
    """
    if not isinstance((active_space_start), int):
        raise TypeError('Only int variables.')
    if not isinstance(qubitop, (list, QubitOperator)):
        raise TypeError('qubit_operators must be a QubitOperator object.')
    start_num_qbts = count_qubits(qubitop)

    new_qubitop = QubitOperator()
    for qop in qubitop:
        new_qubitop += _relabel_single_pauli(qop,
                                             active_space_start,
                                             start_num_qbts)

    return new_qubitop


def _relabel_single_fermi(operator, active_space_start, start_num_qbts):
    """
    Relabel single Pauli operator.

    Args:
        operator (FermionOperator): Operator to relabel.
        active_space_start (int): spatial orbit from where the active space
            starts.
        start_num_qbts (int): number of qubits before reducing active space.
    Returns:
        relabel_operator (FermionOperator): Operator with reduced labels.

    Notes:
        If operator acts on a qubit from frozen orbital, this operator is
        removed.

    Raises:
        TypeError: if operator is not a FermionOperator.
        ValueError: if number of terms in operator is more than 1.
    """
    if not isinstance(operator, FermionOperator):
        raise TypeError('Input must be a FermionOperator.')
    if len(operator.terms) > 1:
        raise ValueError('Input has more than FermionOperator.')
    if list(operator.terms.keys())[0] == ():  # Do nothing if operator is empty
        return operator
    if 2 * active_space_start > start_num_qbts:
        raise ValueError('Starting active space larger than qubits.')

    qbts, cre_ann = zip(*list(operator.terms.keys())[0])

    new_label = []
    for q, t in zip(qbts, cre_ann):
        if q in list(range(2 * active_space_start)):
            return FermionOperator()
        else:
            new_q = (q - 2 * active_space_start, t)
            new_label.append(new_q)  # append tuple of new label

    return FermionOperator(new_label, list(operator.terms.values())[0])


def relabel_fermionoperator(fermiop, active_space_start):
    """
    Relabel fermiop with reduced activate space.

    Args:
        operator (FermionOperator): Operator to relabel.
        active_space_start (int): spatial orbit from where the active space
            starts.
    Returns:
        relabel_operator (FermionOperator): Operator with reduced labels.

    Notes:
        If operator acts on a qubit from frozen orbital, this operator is
        removed.

    Raises:
        TypeError: if operator is not a FermionOperator.
        ValueError: if number of terms in operator is more than 1.
    """
    if not isinstance((active_space_start), int):
        raise TypeError('Only int variables.')
    if not isinstance(fermiop, (list, FermionOperator)):
        raise TypeError('fermiop must be a QubitOperator object.')
    start_num_qbts = count_qubits(fermiop)

    new_fermiop = FermionOperator()
    for fop in fermiop:
        new_fermiop += _relabel_single_fermi(fop,
                                             active_space_start,
                                             start_num_qbts)

    return new_fermiop
