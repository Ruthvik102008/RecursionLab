import { loadPyodide } from 'https://cdn.jsdelivr.net/pyodide/v0.27.5/full/pyodide.mjs';
let py;
try {
  py = await loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.27.5/full/'});
  const response = await fetch('./runner.py?v=20261011');
  if (!response.ok) throw new Error('Could not load the test runner.');
  await py.runPythonAsync(await response.text());
  self.postMessage({type:'ready'});
} catch (e) { self.postMessage({type:'load-error',message:String(e)}); }
self.onmessage = async ({data}) => {
  if (!py) return;
  try {
    const run = py.globals.get('run_json');
    const result = JSON.parse(run(JSON.stringify(data.payload)));
    run.destroy();
    self.postMessage({type:'result',id:data.id,result});
  } catch (e) { self.postMessage({type:'result',id:data.id,result:{ok:false,error:String(e),hint:'Try a smaller input or check for calls that never reach a base case.'}}); }
};
