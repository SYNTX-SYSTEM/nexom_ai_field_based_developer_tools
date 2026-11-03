import { ReactFlow, Background, Controls, type Node, type Edge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
export default function FieldGraph({data}:{data:any}){
const fields=data?.fields||[];const relations=data?.relations||[];
const nodes:Node[]=fields.map((f:any,i:number)=>({id:f.id,position:{x:(i%3)*230,y:Math.floor(i/3)*125},data:{label:f.type+' ('+f.state+')'}}));
const edges:Edge[]=relations.map((r:any)=>({id:r.id,source:r.source,target:r.target,label:r.kind}));
return <div style={{height:330,border:'1px solid #cbd5e1',borderRadius:10,background:'#fff'}}><ReactFlow nodes={nodes} edges={edges} fitView nodesDraggable={false}><Background/><Controls/></ReactFlow></div>;
}
