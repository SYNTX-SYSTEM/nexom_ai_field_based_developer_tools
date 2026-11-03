from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Preformatted,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from pathlib import Path
out=Path(__file__).parent/'NEMOX_AI_RICO7_FINAL_SYSTEM_ARCHITECTURE.pdf'
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='TitleX',parent=styles['Title'],fontSize=20,leading=25,textColor=colors.HexColor('#12384a')))
story=[]
def h(s):story.append(Paragraph(s,styles['Heading2']));story.append(Spacer(1,6))
def p(s):story.append(Paragraph(s,styles['BodyText']));story.append(Spacer(1,9))
story.append(Paragraph('NEMOX AI | RICO-7 FINAL SYSTEM ARCHITECTURE',styles['TitleX']));p('Field-Based Developer Tools | 1 November 2026 | Executable local demonstration')
h('1. Domain logic')
p('A: Freight forwarding users reference prior shipments, constraints and relative dates. The intent inspector preserves the original request, extracts deterministic requirements, exposes candidate shipment references and marks ambiguous context unresolved.')
p('B: An operator reviews an agent-selected carrier. Feedback is tied to an immutable decision, proposed, explicitly confirmed and retrieved only when operation and route match. A subsequent decision records retrieved feedback IDs.')
p('C: A freight request may lack prerequisites. A capability registry defines required attributes and prerequisite edges. A clarification supplies missing values, and the dependency frontier is recalculated.')
h('2. Shared field core')
p('FieldRecord: id, type, scope, state, version, JSON payload, source references and creation timestamp. FieldRelation: source, target, kind, scope, validity and source event. FieldTransition: previous state, next state, triggering event, version and timestamp. FieldRepository implements create/get/transition/relation/graph/reset. FieldContextResolver traverses scoped explicit relations.')
p('Field lifecycle: INITIAL to ENRICHED or UNRESOLVED; ENRICHED to UNRESOLVED or CONFIRMED; UNRESOLVED to ENRICHED or CORRECTED; CORRECTED to CONFIRMED or UNRESOLVED; CONFIRMED to SUPERSEDED. Versions increase on transitions. Invalid transitions and cross-scope relations raise typed validation errors.')
h('3. Component architecture')
story.append(Preformatted('Browser (React, TypeScript, React Flow)\n              | HTTP /api\n        FastAPI application\n         /       |       \\\n Intent module Feedback module Gap module\n         \\       |       /\n      FieldRepository / ContextResolver\n                  |\n               SQLite',styles['Code']))
h('4. Data model')
p('SQLite tables: fields, relations, transitions, decisions, feedback, gaps. Domain modules persist through field core or explicitly scoped SQLite transactions. Each decision captures an immutable JSON context snapshot. Confirmed feedback is also represented by a confirmed field record.')
h('5. API contracts')
for endpoint in ['GET /api/health','POST /api/intent {text,scope}','POST /api/decisions {action,scope,context}','POST /api/feedback {decision_id,scope,correction}','POST /api/feedback/{id}/confirm {scope,accept}','POST /api/subsequent {scope,operation,route,base_action}','GET /api/history/{scope}','POST /api/gaps {text,scope,values}','POST /api/gaps/{id}/resolve {scope,answers}','GET /api/graph/{scope}','POST /api/reset {}']:p(endpoint)
h('6. Processing algorithms')
p('Intent: tokenize by deterministic phrase recognition; identify historical reference; load synthetic shipment candidates; keep ambiguous matches unresolved; persist request, intent, requirement and context fields and explicit edges.')
p('Feedback: persist decision; correlate correction by decision_id and scope; confirm; create field and valid transitions; retrieve confirmed corrections matching both operation and route; emit a new decision with retrieval IDs.')
p('Gap: select capability from request; load required attributes and dependency edges; compute missing attributes; return missing frontier whose predecessors are available; merge supplied answers; reevaluate. Current registry supports cheaper_shipping and booking.')
h('7. RICO-7 reconstruction')
for i,s in enumerate(['Domain: freight RFQs, carrier correction, incomplete shipment requests','Information: source text, candidate shipments, decision context and clarification answers','Semantic: typed requirements, explicit relations and unresolved references','Decision: context snapshots, operational scope and chosen action','Feedback: proposed correction, confirmation and retrieval','State: versioned transitions and retained decision history','Longitudinal: confirmed scope-specific corrections influence subsequent decisions'],1):p(f'R{i}: {s}.')
h('8. Inverse sweep')
p('A inspection output requires request input, extraction, candidate retrieval, field creation and graph relations. B changed subsequent decision requires confirmed correction, matched operation/route, persisted decision and retrieval manifest. C resolved gap requires capability template, missing frontier, clarification answer and reevaluation.')
h('9. Implementation mapping')
for s in ['backend/fieldcore/core.py: field persistence and state transitions','backend/intent_inspector/service.py: Solution A','backend/feedback_engine/service.py: Solution B','backend/gap_detector/service.py: Solution C','backend/api/main.py: HTTP contracts','frontend/src/main.tsx: three views','frontend/src/components/FieldGraph.tsx: relationship visualization','backend/tests/test_system.py: backend integration and domain tests','start.sh: local orchestration','docker-compose.yml: container alternative']:p(s)
h('10. Startup and tests')
p('Local: ./start.sh, then http://localhost:3000. Docker alternative: docker compose up --build. Backend tests: PYTHONPATH=backend python -m pytest -q backend/tests. Frontend: cd frontend &amp;&amp; npm install &amp;&amp; npm run build. Synthetic demo requires no model credentials.')
h('11. Validation status and boundaries')
p('Backend automated tests: five passed. Frontend dependency installation/build and Docker startup were not verified in this execution environment. The solution is a functional local demonstration, not a production integration with nemox private systems. Historical architecture and original source are retained in the archive.')
SimpleDocTemplate(str(out),pagesize=(21*cm,29.7*cm),rightMargin=2*cm,leftMargin=2*cm,topMargin=1.7*cm,bottomMargin=1.7*cm).build(story)
print(out)
