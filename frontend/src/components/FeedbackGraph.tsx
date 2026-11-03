import { ReactFlow, Background, Controls, MarkerType, type Edge, type Node } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

type Decision = {
  id: string;
  action: string;
  context?: { retrieved_feedback_ids?: string[] };
};

type Feedback = {
  id: string;
  decision_id: string;
  status: string;
  correction: Record<string, unknown>;
};

type History = { decisions: Decision[]; feedback: Feedback[] };

/** Module B only: graph relations are derived exclusively from recorded history. */
export default function FeedbackGraph({ data }: { data: History }) {
  const decisions = data.decisions ?? [];
  const feedback = data.feedback ?? [];
  const decisionIds = new Set(decisions.map(d => d.id));
  const feedbackById = new Map(feedback.map(f => [f.id, f]));

  const nodes: Node[] = [
    ...decisions.map((d, index): Node => ({
      id: d.id,
      position: { x: index * 760, y: 140 },
      data: { label: <span><strong>▣ Decision</strong><div>{d.action}</div></span> },
      style: {
        width: 150,
        padding: 12,
        textAlign: 'center',
        color: '#1e3a8a',
        background: '#dbeafe',
        border: '2px solid #2563eb',
        borderRadius: 12,
      },
    })),
    ...feedback.filter(f => decisionIds.has(f.decision_id)).flatMap((f, index): Node[] => {
      const originIndex = decisions.findIndex(d => d.id === f.decision_id);
      const x = originIndex * 760;
      const y = 100 + index * 170;
      const correctedValue = f.correction.preferred_action ?? Object.entries(f.correction)
        .filter(([key]) => !['operation', 'route'].includes(key))
        .map(([, value]) => String(value)).join(', ');
      const color = f.status === 'CONFIRMED' ? '#16a34a' : f.status === 'REJECTED' ? '#dc2626' : '#64748b';
      return [
        {
          id: `correction:${f.id}`,
          position: { x: x + 215, y },
          data: { label: <span><strong>◇ Correction</strong><div>{String(correctedValue)}</div></span> },
          style: {
            width: 175,
            padding: 20,
            textAlign: 'center',
            color: '#92400e',
            background: '#fef3c7',
            border: '2px solid #d97706',
            clipPath: 'polygon(14% 0, 86% 0, 100% 50%, 86% 100%, 14% 100%, 0 50%)',
          },
        },
        {
          id: `feedback:${f.id}`,
          position: { x: x + 475, y: y - 12 },
          data: { label: <span><strong>{f.status === 'CONFIRMED' ? '✓' : f.status === 'REJECTED' ? '×' : '○'}</strong><div>{f.status}</div></span> },
          style: {
            width: 108,
            height: 108,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            color,
            background: f.status === 'CONFIRMED' ? '#dcfce7' : f.status === 'REJECTED' ? '#fee2e2' : '#f1f5f9',
            border: `3px solid ${color}`,
            borderRadius: '50%',
          },
        },
      ];
    }),
  ];

  const edges: Edge[] = [
    ...feedback.filter(f => decisionIds.has(f.decision_id)).flatMap((f): Edge[] => [
      {
        id: `corrects:${f.id}`,
        source: f.decision_id,
        target: `correction:${f.id}`,
        label: 'corrected by',
        markerEnd: { type: MarkerType.ArrowClosed },
      },
      {
        id: `records:${f.id}`,
        source: `correction:${f.id}`,
        target: `feedback:${f.id}`,
        label: f.status.toLowerCase(),
        markerEnd: { type: MarkerType.ArrowClosed },
      },
    ]),
    ...decisions.flatMap((d): Edge[] =>
      (d.context?.retrieved_feedback_ids ?? [])
        .filter(id => feedbackById.get(id)?.status === 'CONFIRMED' && decisionIds.has(feedbackById.get(id)!.decision_id))
        .map(id => ({
          id: `retrieved:${id}:${d.id}`,
          source: `feedback:${id}`,
          target: d.id,
          type: 'bezier',
          label: '↻ retrieved for',
          animated: true,
          style: { stroke: '#16a34a', strokeWidth: 3 },
          markerEnd: { type: MarkerType.ArrowClosed, color: '#16a34a' },
        }))
    ),
  ];

  return <div style={{ height: 440, border: '1px solid #cbd5e1', borderRadius: 10, background: '#fff' }}>
    <ReactFlow nodes={nodes} edges={edges} fitView nodesDraggable={false}>
      <Background />
      <Controls />
    </ReactFlow>
  </div>;
}
