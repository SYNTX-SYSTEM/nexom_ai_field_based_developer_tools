import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import ReactFlow, {Background,Controls} from 'reactflow';
import 'reactflow/dist/style.css';
const title="User Understanding Gap Detector";
function App() {
 const [input,setInput]=useState('Same shipment as last week, but two days earlier.');
 const [result,setResult]=useState<any>(null); const [error,setError]=useState('');
 const endpoint="/api/gaps/analyze";
 async function submit() {try{const body=endpoint==='/api/decisions'?{request:input,carrier:'Carrier A'}:{request:input};const r=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const x=await r.json();if(!r.ok)throw Error(JSON.stringify(x));setResult(x);setError('')}catch(e){setError(String(e))}}
 const nodes=result?[{id:'1',position:{x:0,y:20},data:{label:'User request'}},{id:'2',position:{x:240,y:20},data:{label:'Context field'}},{id:'3',position:{x:480,y:20},data:{label:'Developer inspection'}}]:[];
 const edges=[{id:'e1',source:'1',target:'2'},{id:'e2',source:'2',target:'3'}];
 return <main style={{fontFamily:'system-ui',maxWidth:1000,margin:'32px auto',padding:20}}><h1>{title}</h1><p>Independent field-based developer inspection tool. Synthetic data only.</p><textarea value={input} onChange={e=>setInput(e.target.value)} style={{width:'100%',height:100}}/><p><button onClick={submit}>Process request</button></p>{error&&<p role="alert">{error}</p>}{result&&<><section style={{height:180,border:'1px solid #ddd'}}><ReactFlow nodes={nodes} edges={edges} fitView><Background/><Controls/></ReactFlow></section><h2>Inspection result</h2><pre style={{whiteSpace:'pre-wrap',background:'#f4f5f7',padding:18}}>{JSON.stringify(result,null,2)}</pre></>}</main>
}
createRoot(document.getElementById('root')!).render(<App/>);
