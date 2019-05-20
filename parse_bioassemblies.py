#!/usr/bin/env python3
"""
Parses the biological assemblies of a mmCIF file
For each assembly.
 a list of 4x4 transformation matrices is computed, and returned together
 with a list of chains

Biological assemblies may contain non-protein or fantasy chains; it is possible
 to pass in a list of interesting chains, and the returned chain lists will
 then be filtered accordingly
"""
import sys
import re
from pdbx.reader.PdbxReader import PdbxReader
import copy
import numpy as np

paren_match = re.compile(r'\([^\(\)]*?\)')
identity = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],dtype=float)

def parseOperationExpression(expression):
    operations = []
    if expression.find(",") > -1:
        # comma-separated list of expressions
        sub_expressions = expression.split(",")
        for sub_expression in sub_expressions:
            operations += parseOperationExpression(sub_expression)
    elif expression.find("-") > -1:
        # range
        start, end = expression.split("-")
        start = int(start)
        end = int(end)
        for n in range(start, end + 1):
            operations.append(str(n))
    else:
        # single operation
        operations = [expression]
    return operations

def prepareOperation(oper_list, curr_op, opindex):
    op = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], dtype=float)

    # Prepare matrices for operation
    # Fill the operation matrix and multiply it with the current one
    for i in range(3):
        op[i][3] = float(oper_list.getValue("vector[" + str(i + 1) + "]", opindex))
        for j in range(3):
            op[i][j] = float(oper_list.getValue("matrix[" + str(i + 1) + "][" + str(j + 1) + "]", opindex))

    # Handles Cartesian product expressions (4x4 matrix multiplication)
    """
    operation = copy.deepcopy(op)
    sum_ = 0.0
    for row in range(4):
        for col in range(4):
            sum_ = 0.0
            for r in range(4):
                sum_ += (curr_op[row][r] * op[r][col])
            operation[row][col] = sum_
    """
    operation = curr_op.dot(op)
    return operation

def getOperations(op_id_lists, oper_list, curr_matrix=identity):
    op_id_list = op_id_lists[0]
    opindex = -1
    for op_id in op_id_list:
        # Find the index of the current operation in the oper_list category table
        for row in range(oper_list.getRowCount()) :
            if oper_list.getValue("id", row) == op_id:
                opindex = row
                break
        assert opindex != -1
        new_matrix = prepareOperation(oper_list, curr_matrix, opindex)
        if len(op_id_lists) == 1:
            yield new_matrix
        else:
            new_matrices = getOperations(op_id_lists[1:], oper_list, new_matrix)
            for new_mat in new_matrices:
                yield new_mat

def parse_bioassemblies(cif):
    # Retrieve the pdbx_struct_assembly_gen category table, which details the generation of each macromolecular assembly
    assembly_gen = cif.getObj("pdbx_struct_assembly_gen")

    # Retrieve the pdbx_struct_oper_list category table, which details translation and rotation
    # operations required to generate/transform assembly coordinates
    oper_list = cif.getObj("pdbx_struct_oper_list")

    assemblies = []

    for index in range(assembly_gen.getRowCount()):

        # Retrieve the operation expression for this assembly from the oper_expression attribute
        oper_expression = assembly_gen.getValue("oper_expression", index)

        paren_expressions = [m[1:-1] for m in re.findall(paren_match, oper_expression)]
        if not len(paren_expressions):
            paren_expressions = [oper_expression]

        # Lists to hold the individual operations
        # The operation matrices will be a Cartesian combination of these lists
        op_id_lists = [parseOperationExpression(e) for e in paren_expressions]

        # Retrieve the chain_id_list, which indicates which atoms to apply the operations to
        chain_id_list = assembly_gen.getValue("asym_id_list", index).split(",")

        operations = getOperations(op_id_lists, oper_list)
        assemblies.append((list(operations), chain_id_list))
    return assemblies

if __name__ == "__main__":
    cif_file = sys.argv[1]
    data = []
    PdbxReader(open(cif_file)).read(data)
    cif = data[0]

    assemblies = parse_bioassemblies(cif)
    interesting_chains = set(sys.argv[2:])
    for assembly in assemblies:
        matrices, chains = assembly
        if len(interesting_chains) and not interesting_chains.intersection(set(chains)):
            continue
        print("Chains:")
        print(chains)
        print("Matrices:")
        for matrix in matrices:
            print(matrix)
