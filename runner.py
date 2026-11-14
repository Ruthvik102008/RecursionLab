import ast, contextlib, doctest, io, json, sys, traceback, linecache, types

class LimitedOutput(io.StringIO):
    def write(self, text):
        remaining = 20000 - self.tell()
        if remaining > 0: super().write(text[:remaining])
        return len(text)

def error_hint(exc):
    if isinstance(exc, (SyntaxError, IndentationError)):
        return 'Check punctuation and indentation near the indicated line. Every function and conditional body needs indentation.'
    if isinstance(exc, RecursionError):
        return 'Your calls did not reach a base case soon enough. Trace the next argument for the smallest failing input.'
    if isinstance(exc, NotImplementedError):
        return 'Replace the starter placeholder with your own base case and recursive or iterative step.'
    if isinstance(exc, NameError):
        return 'Check function names and variable spellings. Each problem starts with a fresh namespace; add any helpers it needs in this editor.'
    if isinstance(exc, AttributeError):
        return 'Check the object before the dot: a Tree has label/branches; a Link has first/rest. None and () have neither. A missing return can leave you with None.'
    if isinstance(exc, KeyError):
        return 'Dictionary indexing uses keys. Check membership before a possibly missing lookup, or use a fallback when the contract allows it.'
    if isinstance(exc, IndexError):
        return 'Check whether the list is empty before selecting an element. The last nonnegative index is len(s) - 1, not len(s).'
    if isinstance(exc, TypeError) and 'NoneType' in str(exc):
        return 'One call may be returning None. Check that every branch sends its result back with return.'
    if isinstance(exc, TimeoutError):
        return 'The run took too many steps. Check whether each loop or recursive call moves toward its stopping condition.'
    if isinstance(exc, TypeError):
        return 'Check the number and types of arguments, and the values your helper calls return.'
    return 'Try a smaller input and inspect one step at a time. Check the operation mentioned in the error.'

def describe_error(exc):
    if isinstance(exc, SyntaxError): return f'{type(exc).__name__} on line {exc.lineno}: {exc.msg}'
    frames=traceback.extract_tb(exc.__traceback__)
    line=next((f.lineno for f in reversed(frames) if f.filename=='<your-code>'),None)
    where=f' on line {line}' if line else ''
    return f'{type(exc).__name__}{where}: {str(exc)[:600]}'

def new_namespace():
    module = types.ModuleType('__practice__')
    sys.modules['__practice__'] = module
    return module.__dict__

def style_check(tree, problem):
    # lesson extension checks: supplied traversal/display helpers do not count
    # toward the student's required approach.
    for expected in problem.get('scaffoldSyntax', []):
        actual = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == expected['name']), None)
        if actual is None or ast.dump(actual, include_attributes=False) != expected['ast']:
            return 'Keep the supplied '+expected['name']+' definition unchanged. Write your solution below the scaffold.'
    excluded = set(problem.get('scaffoldNames', []))
    if excluded:
        tree = ast.Module(body=[n for n in tree.body if not
            (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in excluded)], type_ignores=[])
    def annotation_text(node):
        if node is None: return ''
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value.replace(' ', '')
        return ast.unparse(node).replace(' ', '')
    functions = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    for name, expected in problem.get('annotations', {}).items():
        function = functions.get(name)
        if function is None: return f'Define {name} with the requested annotations.'
        actual = {arg.arg: arg.annotation for arg in function.args.args}
        actual['return'] = function.returns
        for field, hint in expected.items():
            if annotation_text(actual.get(field)) != hint.replace(' ', ''):
                return f'Keep the requested {field} annotation for {name}. Type hints document the contract separately from its calculation.'
    class_nodes = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
    for name, fields in problem.get('classes', {}).items():
        node = class_nodes.get(name)
        if node is None: return f'Define the {name} data class.'
        decorators = {ast.unparse(d).split('(')[0].split('.')[-1] for d in node.decorator_list}
        if 'dataclass' not in decorators: return 'Apply the dataclass decorator to the class you define.'
        actual = {n.target.id: n.annotation for n in node.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)}
        for field, hint in fields.items():
            if annotation_text(actual.get(field)) != hint.replace(' ', ''):
                return f'Define the annotated {field} field inside {name}, using the type specified in the prompt.'
    if 'generic' in problem.get('required', []) and not any(getattr(n, 'type_params', []) for n in functions.values()):
        return 'Declare the generic type variable in square brackets after the function name.'

    mode=problem['mode']
    defs={n.name:n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    edges={name:set() for name in defs}
    for name,node in defs.items():
        for sub in ast.walk(node):
            if isinstance(sub,ast.Call) and isinstance(sub.func,ast.Name) and sub.func.id in defs:
                edges[name].add(sub.func.id)
    def reaches(start,current,seen):
        return any(target==start or (target not in seen and reaches(start,target,seen|{target})) for target in edges.get(current,()))
    cycles={name for name in defs if reaches(name,name,{name})}
    loops=any(isinstance(n,(ast.For,ast.While,ast.AsyncFor,ast.ListComp,ast.SetComp,ast.DictComp,ast.GeneratorExp)) for n in ast.walk(tree))
    nodes=list(ast.walk(tree))
    node_types={type(n).__name__ for n in nodes}
    call_names={n.func.id if isinstance(n.func,ast.Name) else n.func.attr for n in nodes if isinstance(n,ast.Call) and isinstance(n.func,(ast.Name,ast.Attribute))}
    if mode=='tree_walk' and not cycles:
        return 'Use recursive calls on smaller branches. A fixed number of indexing steps cannot handle arbitrary depth.'
    if mode=='for_loop':
        if not any(isinstance(n,ast.For) for n in nodes):
            return 'Use a for statement to visit the sequence in this exercise. Put the running result before the loop and the final return after it.'
        if cycles: return 'Practice iteration here: carry the result through a for loop instead of making recursive calls.'
    if mode=='listcomp':
        if 'ListComp' not in node_types: return 'This exercise asks for a list comprehension. Identify the input sequence, the output expression, and any filter.'
        if any(isinstance(n,(ast.For,ast.While)) for n in nodes) or cycles:
            return 'Build this result with a list comprehension instead of a loop statement or recursive call.'
    if mode=='dictcomp':
        if 'DictComp' not in node_types: return 'Use a dictionary comprehension: key expression, value expression, source, and any filter.'
        if any(isinstance(n,(ast.For,ast.While)) for n in nodes) or cycles:
            return 'Use comprehensions here instead of loop statements or recursion.'
    for requirement in problem.get('required',[]):
        if requirement=='unpack':
            present=any(isinstance(n,ast.For) and isinstance(n.target,(ast.Tuple,ast.List)) and len(n.target.elts)==2 for n in nodes)
        elif requirement=='generic': present=any(getattr(n, 'type_params', []) for n in defs.values())
        else: present=requirement in node_types or requirement in call_names or requirement in defs or any(isinstance(n, ast.Name) and n.id == requirement for n in nodes)
        if not present:
            return {'unpack':'Unpack each pair into two names in the for-loop header.', 'Slice':'Use a slice to give the recursive call a shorter list.', 'Subscript':'Use indexing to select the needed list element.', 'In':'Use the in operator to check whole-element membership.', 'NotIn':'Use not in to express absence.'}.get(requirement,f'This task asks you to use {requirement}. Re-read the requested approach.')
    for forbidden in problem.get('forbidden',[]):
        if (forbidden=='loops' and loops) or forbidden in node_types or forbidden in call_names:
            return 'This solution uses an approach excluded by the prompt. Check the requested list operation and the shortcuts it asks you to avoid.'
    if mode in ('recursive','mutual','tail','tree'):
        if loops: return 'This exercise asks for recursion. Replace repeated work in loops or comprehensions with a smaller function call.'
        if not cycles: return 'The examples need a recursive solution here. Which function should call itself, directly or through a helper?'
    if mode=='tree' and not any(sum(isinstance(sub,ast.Call) and isinstance(sub.func,ast.Name) and sub.func.id==name for sub in ast.walk(node))>=2 for name,node in defs.items()):
        return 'This problem asks you to explore more than one smaller case. Check that you have recursive calls for both choices.'
    if mode=='higher' and loops:
        return 'Use the ordering helper and recursive callbacks here instead of a loop.'
    if mode=='iterative':
        if cycles: return 'This exercise asks for iteration. Carry changing values in loop variables instead of recursive calls.'
        if not loops: return 'Use a loop for the repeated work in this exercise.'
    for caller,callee in problem.get('calls',[]):
        if callee not in edges.get(caller,set()): return f'Check the relationship between {caller} and {callee}. This task needs a call from the first to the second.'
    if mode=='tail':
        parents={child:parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in cycles:
                parent=parents.get(node)
                if not isinstance(parent,ast.Return) or parent.value is not node:
                    return 'Carry the updated accumulator into the next call and return that call directly. Leave no calculation waiting afterward.'
    if problem['id'] in (3,4,105) and any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('str','repr') for n in ast.walk(tree)):
        return 'Use arithmetic to split off digits instead of converting the number to text.'
    if problem['id']==19 and any(isinstance(n,ast.Pow) or (isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='pow') for n in ast.walk(tree)):
        return 'Build the power from smaller calls. This exercise excludes ** and pow.'
    if problem['id']==201:
        if not any('next_smaller_coin' in targets for name,targets in edges.items() if name!='next_smaller_coin'):
            return 'Use next_smaller_coin to move between allowed denominations. Subtracting one from a denomination introduces coin values that are not allowed.'
    return None

class HintRunner(doctest.DocTestRunner):
    def __init__(self,hint,hidden=False,printing=False):
        super().__init__(optionflags=0)
        self.rows=[]; self.hint=hint; self.hidden=hidden; self.printing=printing
    def report_success(self,out,test,example,*args): pass
    def report_failure(self,out,test,example,got):
        hint=self.hint
        if self.printing and not got.strip() and example.want.strip():
            hint='No lines were printed for this call. Check that the stopping condition does not skip a required print, and where printing belongs relative to the smaller call.'
        elif not self.printing and (got.strip()=='None' or (not got.strip() and example.want.strip())):
            hint='This call may be returning None. Check that the result is returned on every path, including the recursive path.'
        self.rows.append(dict(kind='mismatch',call=example.source.strip(),actual=got[:1200] if not self.hidden else None,hint=hint))
    def report_unexpected_exception(self,out,test,example,exc_info):
        exc=exc_info[1]
        self.rows.append(dict(kind='error',call=example.source.strip(),error=describe_error(exc),hint=error_hint(exc)))

def run_payload(payload):
    problem=payload['problem']; code=payload['code']; mode=payload['mode']
    output=LimitedOutput(); ns=new_namespace()
    try:
        linecache.cache['<your-code>']=(len(code),None,code.splitlines(keepends=True),'<your-code>')
        tree=ast.parse(code,filename='<your-code>')
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
            exec(compile(tree,'<your-code>','exec'),ns)
    except Exception as exc:
        return dict(ok=False,error=describe_error(exc),hint=error_hint(exc),output=output.getvalue())
    if mode=='scratch':
        try:
            scratch=ast.parse(payload['scratch'],filename='<your-input>')
            with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):
                if scratch.body and isinstance(scratch.body[-1],ast.Expr):
                    last=scratch.body.pop()
                    exec(compile(scratch,'<your-input>','exec'),ns)
                    value=eval(compile(ast.Expression(last.value),'<your-input>','eval'),ns)
                    if value is not None: print(repr(value))
                else: exec(compile(scratch,'<your-input>','exec'),ns)
            return dict(ok=True,output=output.getvalue() or '(No output. Try a function call or print statement.)')
        except Exception as exc:
            return dict(ok=False,error=describe_error(exc),hint=error_hint(exc),output=output.getvalue())
    style=style_check(tree,problem); parser=doctest.DocTestParser()
    try:
        test=parser.get_doctest(payload['doctests'],ns.copy(),'Your doctests','<your-doctests>',0)
        if not test.examples: return dict(ok=False,error='No doctests found.',hint='Add a call beginning with >>> and put its expected output on the following line.')
        runner=HintRunner(problem['hint'],printing=problem.get('printing', False) or 101<=problem['id']<=110); result=runner.run(test,out=lambda _:None)
    except Exception as exc:
        return dict(ok=False,error=describe_error(exc),hint='Check your doctest formatting: >>> call, then its expected output on the next line.')
    core_rows=[]; core_passed=0
    for check in problem['checks']:
        fresh=new_namespace()
        with contextlib.redirect_stdout(LimitedOutput()),contextlib.redirect_stderr(LimitedOutput()): exec(compile(tree,'<your-code>','exec'),fresh)
        core=parser.get_doctest('>>> '+check['source']+'\n'+check['want']+'\n',fresh,'Core check','<core-check>',0)
        checker=HintRunner(check['hint'],hidden=True,printing=problem.get('printing', False) or 101<=problem['id']<=110); checked=checker.run(core,out=lambda _:None)
        if checked.failed==0: core_passed+=1
        core_rows.extend(checker.rows)
    return dict(ok=not style and result.failed==0 and core_passed==len(problem['checks']),style=style,
                publicPassed=result.attempted-result.failed,publicTotal=result.attempted,
                corePassed=core_passed,coreTotal=len(problem['checks']),rows=(runner.rows+core_rows)[:5],output=output.getvalue())

def run_json(payload_json):
    payload=json.loads(payload_json)
    coins=payload.get('problem',{}).get('id')==201
    step_limit=2000000 if coins else 60000
    steps=0
    def limit(frame,event,arg):
        nonlocal steps
        if event=='line' and frame.f_code.co_filename in ('<your-code>','<your-input>'):
            steps+=1
            if steps>step_limit: raise TimeoutError('Execution stopped after too many steps.')
        return limit
    sys.setrecursionlimit(1000 if coins else 250)
    try:
        sys.settrace(limit); result=run_payload(payload)
    except BaseException as exc: result=dict(ok=False,error=describe_error(exc),hint=error_hint(exc))
    finally: sys.settrace(None)
    return json.dumps(result)
