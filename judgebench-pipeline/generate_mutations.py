import re

def generate_mutations(source_code):
    mutations = []
    
    # Mutation 1: Change arithmetic operators
    arithmetic_ops = {
        '+': '-',
        '-': '+',
        '*': '/',
        '/': '*',
        '%': '*'
    }
    
    for op, replacement in arithmetic_ops.items():
        mutated_code = re.sub(r'(?<!\w){}(?!\w)'.format(re.escape(op)), replacement, source_code)
        if mutated_code != source_code:
            mutations.append(mutated_code)
    
    # Mutation 2: Change relational operators
    relational_ops = {
        '==': '!=',
        '!=': '==',
        '<': '>=',
        '>': '<=',
        '<=': '>',
        '>=': '<'
    }
    
    for op, replacement in relational_ops.items():
        mutated_code = re.sub(r'(?<!\w){}(?!\w)'.format(re.escape(op)), replacement, source_code)
        if mutated_code != source_code:
            mutations.append(mutated_code)
    
    # Mutation 3: Change logical operators
    logical_ops = {
        '&&': '||',
        '||': '&&'
    }
    
    for op, replacement in logical_ops.items():
        mutated_code = re.sub(r'(?<!\w){}(?!\w)'.format(re.escape(op)), replacement, source_code)
        if mutated_code != source_code:
            mutations.append(mutated_code)
    
    # Mutation 4: Negate conditions
    condition_patterns = [
        r'if\s*\(([^)]+)\)',
        r'while\s*\(([^)]+)\)',
        r'for\s*\(([^;]+);([^;]+);([^)]+)\)'
    ]
    
    for pattern in condition_patterns:
        matches = re.findall(pattern, source_code)
        for match in matches:
            if isinstance(match, tuple):
                condition = match[0]
            else:
                condition = match
            negated_condition = f'!({condition})'
            mutated_code = source_code.replace(condition, negated_condition)
            if mutated_code != source_code:
                mutations.append(mutated_code)
    
    return mutations