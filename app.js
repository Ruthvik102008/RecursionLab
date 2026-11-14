(() => {
'use strict';
const $=id=>document.getElementById(id), problems=window.EXERCISES;
const key=window.LESSON_CONFIG?.storageKey||'recursion-lab-v1';
let drafts={}, selected=0, worker=null, ready=false, pending=null, timer=null, serial=0, busy=false;
try { const saved=JSON.parse(localStorage.getItem(key)||'{}'); drafts=saved.drafts||{}; selected=Math.max(0,Math.min(problems.length-1,saved.selected||0)); } catch {}
const modeLabels={tree_walk:'Use recursion on branches. Loops and comprehensions over branches are allowed.',dictcomp:'Use a dictionary comprehension. Follow the additional constraints in the prompt.',for_loop:'Use a for loop. Follow any additional constraints in the prompt.',listcomp:'Use a list comprehension. No loop statements or recursion.',recursive:'Use recursion. No loops or comprehensions.',mutual:'Use mutual recursion. No loops or comprehensions.',tree:'Use tree recursion: branch into smaller calls. No loops or comprehensions.',higher:'Use functions as arguments to arrange the recursive calls. No loops or comprehensions.',tail:'Use accumulator recursion; return the recursive call directly. No loops.',iterative:'Use a loop. No recursive calls.',any:'Follow the approach specified in the prompt.'};
function draft(){return drafts[problems[selected].id]||(drafts[problems[selected].id]={code:problems[selected].starter,doctests:problems[selected].doctests,scratch:problems[selected].scratch,passed:false});}
function persist(){try{localStorage.setItem(key,JSON.stringify({drafts,selected}));$('saved').textContent='Draft saved on this device';}catch{$('saved').textContent='Saving unavailable in this browser';}}
function capture(){const d=draft();d.code=$('code').value;d.doctests=$('doctests').value;d.scratch=$('scratch').value;persist();}
function drawProgress(){const count=problems.filter(p=>drafts[p.id]?.passed).length;$('progress').textContent=`${count} / ${problems.length} complete`;document.querySelectorAll('#exercise-list button').forEach((b,i)=>{b.setAttribute('aria-current',i===selected?'true':'false');b.textContent=`${drafts[problems[i].id]?.passed?'✓':String(i+1).padStart(2,'0')}  ${problems[i].title}`;});}
$('shortcut').textContent = 'Ctrl / ⌘ + Enter to test · Ctrl / ⌘ + ] to indent';
  const pythonTokens = /(?<comment>#[^\n]*)|(?<string>"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\[^\n]|[^"\\\n])*"?|'(?:\\[^\n]|[^'\\\n])*'?)|(?<prompt>^\s*>>>|^\s*\.\.\.)|(?<number>\b(?:0[xX][\da-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|\d[\d_]*(?:\.[\d_]*)?(?:[eE][+-]?[\d_]+)?))|(?<word>[\p{ID_Start}_][\p{ID_Continue}]*)|(?<operator>[+*/%=<>!&|^~@:-]+)/gmu;
  const keywords = new Set('and as assert async await break case class continue def del elif else except False finally for from global if import in is lambda match None nonlocal not or pass raise return True try while with yield'.split(' '));
  const builtins = new Set('abs all any bool dict enumerate float int len list max min print range reversed set sorted str sum tuple type zip'.split(' '));

  function addSyntaxColors(editor) {
    const frame = document.createElement('div');
    frame.className = 'code-frame';
    const backdrop = document.createElement('pre');
    backdrop.className = 'code-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');
    editor.before(frame);
    frame.append(backdrop, editor);
    editor.wrap = 'off';

    function syncScroll() {
      backdrop.scrollTop = editor.scrollTop;
      backdrop.scrollLeft = editor.scrollLeft;
    }

    function repaint() {
      const source = editor.value;
      const tokens = document.createDocumentFragment();
      let end = 0;
      for (const match of source.matchAll(pythonTokens)) {
        const [token] = match;
        const group = Object.keys(match.groups).find(name => match.groups[name] !== undefined);
        const kind = group === 'word'
          ? keywords.has(token) ? 'keyword' : builtins.has(token) ? 'builtin' : null
          : group;
        tokens.append(source.slice(end, match.index));
        if (kind) {
          const span = document.createElement('span');
          span.className = 'token-' + kind;
          span.textContent = token;
          tokens.append(span);
        } else {
          tokens.append(token);
        }
        end = match.index + token.length;
      }
      tokens.append(source.slice(end), '\n');
      backdrop.replaceChildren(tokens);
      syncScroll();
    }

    editor.addEventListener('input', repaint);
    editor.addEventListener('scroll', syncScroll, {passive: true});
    repaint();
    return repaint;
  }

  const repaintEditors = ['code', 'doctests', 'scratch'].map(id => addSyntaxColors($(id)));
  const brand = document.querySelector('.brand');
  const mark = document.createElement('span');
  mark.className = 'brand-mark';
  mark.setAttribute('aria-hidden', 'true');
  mark.textContent = '↻';
  const wordmark = document.createElement('strong');
  wordmark.textContent = 'Recursion Lab';
  brand.replaceChildren(mark, wordmark);

  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let rebound;
  motion.addEventListener('change', () => rebound?.cancel());
  window.addEventListener('wheel', event => {
    if (motion.matches || event.ctrlKey || !event.deltaY ||
        event.target.closest('textarea, select, pre')) return;
    const scroller = document.scrollingElement;
    const atTop = scroller.scrollTop <= 0 && event.deltaY < 0;
    const atBottom = scroller.scrollTop + scroller.clientHeight >= scroller.scrollHeight - 1 && event.deltaY > 0;
    if ((!atTop && !atBottom) || rebound?.playState === 'running') return;
    const panel = $('practice').hidden ? $('notes') : $('practice');
    const distance = Math.min(10, Math.abs(event.deltaY) / 9) * (atTop ? 1 : -1);
    rebound = panel.animate(
      [{translate: '0 0'}, {translate: '0 ' + distance + 'px', offset: .32}, {translate: '0 0'}],
      {duration: 420, easing: 'cubic-bezier(.22,.75,.25,1)'}
    );

  }, {passive: true});

function clearResult(){document.querySelector('.feedback').classList.remove('error');$('result-title').textContent='Ready for your attempt';$('result-message').textContent='Run the doctests and core checks. Hints will point you toward the issue without giving you a solution.';$('results').replaceChildren();}
function select(index){if(busy)return;capture();selected=index;const p=problems[index],d=draft();$('exercise-select').value=String(index);$('topic').textContent=p.topic;$('problem-title').textContent=`${String(index+1).padStart(2,'0')} · ${p.title}`;$('prompt').textContent=p.prompt;if($('practice-hint')){$('practice-hint').textContent=p.hint;$('practice-hint').closest('details').open=false;}$('constraint').textContent=modeLabels[p.mode];$('code').value=d.code;$('doctests').value=d.doctests;$('scratch').value=d.scratch;$('scratch-output').textContent='Your output appears here.';clearResult();drawProgress();persist();}
problems.forEach((p,i)=>{const o=document.createElement('option');o.value=i;o.textContent=`${String(i+1).padStart(2,'0')} · ${p.title}`;$('exercise-select').append(o);const b=document.createElement('button');b.type='button';b.onclick=()=>select(i);$('exercise-list').append(b);});
$('exercise-select').onchange=e=>select(Number(e.target.value));
{const d=draft();$('code').value=d.code;$('doctests').value=d.doctests;$('scratch').value=d.scratch;select(selected);}
for(const id of ['code','doctests','scratch']){
  $(id).addEventListener('input',()=>{capture();if(id!=='scratch'){draft().passed=false;persist();drawProgress();$('result-title').textContent='Changed since your last test';$('result-message').textContent='Test this version to check your changes.';$('results').replaceChildren();}});
  $(id).addEventListener('keydown',e=>{if(e.key===']'&&(e.ctrlKey||e.metaKey)&&!e.altKey&&!e.shiftKey){e.preventDefault();const el=e.target,start=el.selectionStart,end=el.selectionEnd;el.setRangeText('    ',start,end,'end');el.dispatchEvent(new Event('input'));}if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();run(id==='scratch'?'scratch':'test');}});
}
function setBusy(value){busy=value;$('test').disabled=value;$('run').disabled=value;$('stop').disabled=!value;$('exercise-select').disabled=value;document.querySelectorAll('#exercise-list button').forEach(b=>b.disabled=value);for(const id of ['code','doctests','scratch'])$(id).readOnly=value;}
function kill(){worker?.terminate();worker=null;ready=false;clearTimeout(timer);}
function finish(result){const task=pending;if(!task)return;clearTimeout(timer);pending=null;setBusy(false);if(task.mode==='scratch'){$('scratch-output').textContent=[result.output,result.error,result.hint&&'Hint: '+result.hint].filter(Boolean).join('\n\n')||'No output.';}else{showResult(result);draft().passed=!!result.ok;persist();drawProgress();}task.resolve(result);}
function showResult(r){document.querySelector('.feedback').classList.toggle('error',!r.ok);$('result-title').textContent=r.ok?'All checks passed':r.error?'This run needs a fix':'Keep going — use the hint below';$('result-message').textContent=r.error?`${r.error}\n${r.hint||''}`:`Your doctests: ${r.publicPassed} / ${r.publicTotal} passed · Core checks: ${r.corePassed} / ${r.coreTotal} passed${r.ok?' · Required approach checked.':''}`;$('results').replaceChildren();if(r.style)addRow('Approach hint',r.style);for(const row of r.rows||[]){const details=[row.error,row.actual!==undefined&&row.actual!==null?`Your output: ${row.actual.trim()||'(no output)'}`:null,'Hint: '+row.hint].filter(Boolean).join('\n');addRow(row.call,details);}if(r.output)addRow('Printed while defining your code',r.output);}
function addRow(title,message){const row=document.createElement('div');row.className='result-row';const h=document.createElement('strong');h.textContent=title;const p=document.createElement('pre');p.textContent=message;row.append(h,p);$('results').append(row);}
function dispatch(){if(!pending)return;const task=pending;$('runtime').textContent='Running Python…';clearTimeout(timer);timer=setTimeout(()=>{kill();$('runtime').textContent='Stopped a long-running program';finish({ok:false,error:'Time limit reached.',hint:'Check whether your loop or recursive call moves toward a stopping condition. Try a smaller input.'});},window.LESSON_CONFIG?.runTimeout||6000);worker.postMessage({id:task.id,payload:task.payload});}
function boot(){
  $('runtime').textContent='Loading Python for the first run…';
  try {worker=new Worker('./worker.js?v=20261011',{type:'module'});}catch(e){finish({ok:false,error:'Python could not start.',hint:'Reload this page in a current browser, then try again.'});return;}
  timer=setTimeout(()=>{kill();$('runtime').textContent='Python could not load';finish({ok:false,error:'Python loading timed out.',hint:'Check your internet connection and try Test code again.'});},90000);
  worker.onmessage=({data})=>{if(data.type==='ready'){ready=true;dispatch();}else if(data.type==='load-error'){kill();$('runtime').textContent='Python could not load';finish({ok:false,error:'Could not load Python.',hint:'Check your internet connection, then try again. Your draft is still saved.'});}else if(data.type==='result'&&data.id===pending?.id){$('runtime').textContent='Python ready · code runs in your browser';finish(data.result);}};
  worker.onerror=()=>{kill();$('runtime').textContent='Python stopped';finish({ok:false,error:'The Python worker stopped unexpectedly.',hint:'Try again. If it repeats, reduce your input size and check for unbounded recursion.'});};
}
async function run(mode){if(busy)return {ok:false,error:'A run is already active.'};capture();setBusy(true);if(mode==='test'){$('result-title').textContent='Checking your code…';$('result-message').textContent='Running your doctests and the core checks.';$('results').replaceChildren();}else $('scratch-output').textContent='Running…';return new Promise(resolve=>{pending={id:++serial,mode,resolve,payload:{mode,problem:problems[selected],code:$('code').value,doctests:$('doctests').value,scratch:$('scratch').value}};if(ready)dispatch();else boot();});}
$('test').onclick=()=>run('test');$('run').onclick=()=>run('scratch');$('stop').onclick=()=>{kill();$('runtime').textContent='Stopped · ready to restart';finish({ok:false,error:'Run stopped.',hint:'Your code is saved. Change the input or stopping condition, then try again.'});};
for(const name of ['practice','notes'])$(name+'-tab').onclick=()=>{for(const view of ['practice','notes']){$(view).hidden=view!==name;$(view+'-tab').setAttribute('aria-pressed',String(view===name));}};
if(document.modelContext?.registerTool){try{Promise.resolve(document.modelContext.registerTool({name:'read_practice_state',description:'Read the selected recursion exercise and its current visible feedback; does not reveal solutions.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute(input){if(!input||Object.keys(input).length)throw new Error('Expected an empty object.');return {exercise:problems[selected].title,code:$('code').value,feedback:$('result-title').textContent+' '+$('result-message').textContent};}})).catch(()=>{});}catch{}}
})();
