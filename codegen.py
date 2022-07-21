template = '''
int main() {
    <<!statements>>
}
'''

def gen(program):
    c_statements = [gen_statement(s) for s in program]
    return template.replace('<<!statements>>', '\n'.join(c_statements))
    
    