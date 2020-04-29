from openfermion import QubitOperator
from openfermion import FermionOperator

def relabel_fermi_operator(fermi_operators,active_space_start):
    '''
    Replaces the labels of a fermionic operator to be within the active space.
    
    Args:
        fermi_operators    (list, FermionOperator): List or FermionOperator of excitations.
        active_space_start (int): spatial orbit from where the active space starts.
    
    Returns:
        relab_operator (FermionOperator): The relabeled version of the fermi_operators
    '''
    if not isinstance(fermi_operators, (list, FermionOperator)):
        raise TypeError('fermi_operators must be a FermionOperator object.')
        
    relab_operator = FermionOperator('1', 1.0)
    relab_operator += - FermionOperator('1', 1.0) #Start with the FermionOperator type
    
    for operator in fermi_operators:        
        qubits  = list(operator.terms.keys())[0]
        temp_term = [] #make list to store relabeled terms
        for i in range(len(qubits)):
            temp_term.append((qubits[i][0]-2*active_space_start,qubits[i][1])) #append tuple of new label

        relab_operator += FermionOperator(temp_term, list(operator.terms.values())[0])

    return relab_operator

def relabel_pauli_operator(qubit_operators, active_space_start):
    '''
    Replaces the labels of a qubit operator to be within the active space.
    
    Args:
        pauli_operators    (list, QubitOperator): List or QubitOperator of Paulis.
        active_space_start (int): spatial orbit from where the active space starts.
    
    Returns:
        relab_qubitop (QubitOperator): The relabeled version of the pauli_operators
    '''
    if not isinstance(qubit_operators, (list, QubitOperator)):
        raise TypeError('qubit_operators must be a QubitOperator object.')
        
    relab_qubitop = QubitOperator('X0', 0.0)
    relab_qubitop += - QubitOperator('X0', 0.0) #Start with the QubitOperator type
    
    for pauli in qubit_operators:        
        qubits, paus = zip(*list(pauli.terms.keys())[0])
        temp_term = ' '
        for i in range(len(paus)):
            temp_term += paus[i]+str(qubits[i]-2*active_space_start)+' '
            
        relab_qubitop += QubitOperator(temp_term,list(pauli.terms.values())[0])
        
    return relab_qubitop