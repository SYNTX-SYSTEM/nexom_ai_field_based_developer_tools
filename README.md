# 🧬 NEMOX AI RICO-7
## Field-Based Developer Tools for Understanding Users

**From problem reconstruction to executable systems.**

> 🧠 Architecture first.  
> 🔗 Relations before isolated components.  
> 🔄 Feedback before static assumptions.  
> ⚡ Implementation follows coherence.

**Architecture:** SYNTX Field-Based System Architecture  
**Author:** Ottavio Braun  
**Date:** November 2026  
**Status:** Executable research prototype  
**License:** Proprietary. All rights reserved.

---

# 🚀 The Story

## Six hours. One challenge. Three developer tools.

On November 1, 2026, nemox AI hosted a hackathon in Munich.

The challenge:

**Build Developer Tools to Better Understand Users.**

A conventional approach might begin by implementing individual features.

RICO-7 began somewhere else.

With the system.

Before generating application code, the challenge was reconstructed through the SYNTX architectural approach.

The objective was to identify the relationships that make user understanding possible:

- What does the user intend?
- Which context influences that intention?
- Which information is missing?
- Which decisions depend on other decisions?
- What happens when a user corrects the system?
- How can that correction influence subsequent interactions?
- How can these relationships remain observable?

These questions produced a shared field-based architecture.

From that architecture, three interconnected developer tools were derived.

The initial architecture was developed in approximately one hour.

The prototype implementation followed in approximately two hours.

By 17:00, the engineering package had been sent to the nemox AI team, ahead of the scheduled 19:00 presentations.

The result was not simply a collection of demos.

It was an extensible technical foundation.

---

# 🧠 The Architectural Idea

## Understanding is relational.

A user's message does not exist in isolation.

Its meaning depends on context, references, previous decisions, missing information and subsequent feedback.

RICO-7 models these relationships through a shared field-based system.

```text
                  USER INPUT
                      │
                      ▼
             CONTEXT RECONSTRUCTION
                      │
                      ▼
               SHARED FIELD CORE
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
     MODULE A      MODULE B      MODULE C
    Intent &       Feedback &    Understanding
    Context        Decision      Gap Detection
    Inspector      Trace
         │            │            │
         └────────────┼────────────┘
                      ▼
              FIELD RELATIONSHIPS
                      │
                      ▼
             STATE & FEEDBACK
                      │
                      ▼
              UPDATED CONTEXT
```

The three modules operate on a common architectural foundation.

This enables shared context, traceable decisions and structured extension.

---

# 🧩 The Three Developer Tools

## 🔍 Module A: User Intent & Context Inspector

**What is the user actually asking for?**

Module A reconstructs intent and contextual dependencies from user input.

Its prototype includes deterministic extraction logic for freight-related requests.

It identifies relevant constraints and unresolved references.

### Capabilities

- Intent and context inspection
- Constraint extraction
- Reference identification
- Contextual dependency representation
- Structured output for downstream processing

### Architectural role

Module A establishes the initial interpretation of the user's request.

Its results provide context for subsequent decisions and gap detection.

---

## 🔄 Module B: Recursive Feedback & Decision Trace Engine

**What changes when the user corrects a decision?**

Module B records decisions, corrections and feedback relationships.

It makes the resulting structures visible through an interactive graph.

The prototype can reuse confirmed corrections when matching operational conditions are encountered again.

### Capabilities

- Decision recording
- Feedback capture
- Correction tracking
- Decision trace visualization
- Context-dependent feedback reuse
- Interactive graph exploration

### Architectural role

Module B connects decisions with their consequences and subsequent corrections.

Feedback becomes part of the evolving system context.

### 🎨 Visual interaction

The React frontend uses an interactive graph to display relationships between decisions and feedback.

Nodes and connections make system relationships directly inspectable.

This is where field-based architecture becomes visually tangible.

---

## 🧭 Module C: User Understanding Gap Detector

**What does the system still need to know?**

Module C identifies missing information and unresolved dependencies.

Rather than treating every missing value as an isolated problem, it examines which gaps block further processing.

### Capabilities

- Required-information inspection
- Missing-field detection
- Dependency frontier identification
- Clarification question generation
- Completeness updates

### Architectural role

Module C identifies where additional user interaction is required.

It provides a structured basis for resolving incomplete context.

---

# 🏗️ Shared Technical Architecture

The prototype uses a common backend architecture and persistent field model.

### Backend

- Python
- FastAPI
- SQLite
- FieldRepository
- FieldContextResolver
- Eleven API operations
- Explicit state and transition handling

### Frontend

- React
- Vite
- Interactive graph visualization
- Module-specific interfaces

### Data model

The SQLite persistence layer includes six principal tables:

```text
fields
relations
transitions
decisions
feedback
gaps
```

Together, they support the representation of field relationships, decisions, feedback and understanding gaps.

---

# 🧬 SYNTX: Architecture Before Implementation

RICO-7 follows a field-based engineering process.

```text
SYSTEM OBSERVATION
        │
        ▼
PROBLEM RECONSTRUCTION
        │
        ▼
FIELD & RELATION ANALYSIS
        │
        ▼
DEPENDENCY IDENTIFICATION
        │
        ▼
ARCHITECTURE DESIGN
        │
        ▼
RECURSIVE COHERENCE REVIEW
        │
        ▼
IMPLEMENTATION SPECIFICATION
        │
        ▼
SOURCE CODE GENERATION
        │
        ▼
INTEGRATION & TESTING
        │
        ▼
EXECUTABLE PROTOTYPE
```

The central principle:

**The implementation is derived from the architecture.**

The architecture defines the intended relationships, boundaries, states and dependencies.

The implementation expresses those structures in executable form.

This separation is particularly relevant to AI-assisted software development, where source code can be generated rapidly.

---

# ⚙️ Getting Started

## Project structure

```text
nemox-developer-tools/
├── backend/
├── frontend/
├── docs/
├── legacy/
├── docker-compose.yml
├── start.sh
└── README.md
```

## Prerequisites

- Python 3
- Python virtual environment support
- Node.js and npm
- A Unix-compatible shell

## Start locally

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r backend/requirements.txt

cd frontend
npm install
cd ..

./start.sh
```

### Local endpoints

| Component | Address |
|---|---|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |
| API documentation | http://localhost:8000/docs |

### Docker

A Docker Compose configuration is included.

```bash
docker compose up --build
```

Check the included Compose configuration for service-specific settings.

---

# 🧪 Verification

The documented backend verification run completed with:

**5 / 5 backend tests passing.**

The engineering package also includes operational and verification documentation.

This result does not imply complete test coverage.

Frontend production builds, container startup and browser end-to-end testing require separate verification in the target environment.

---

# 📚 Engineering Documentation

RICO-7 includes a three-volume engineering documentation package.

### 📘 Volume I: Complete Technical Architecture

Architecture, system relationships, components, interfaces, state transitions and implementation structure.

### 📗 Volume II: Module and Developer Guide

Module responsibilities, technical integration and development guidance.

### 📙 Volume III: Operations & Verification

Startup procedures, operational information and recorded verification results.

**Total: 34 pages of engineering documentation.**

The documentation distinguishes between implemented capabilities, derived architectural elements, conceptual structures and proposed extensions.

---

# 🔮 Extension Potential

The shared field architecture provides several possible development paths.

### 🤖 AI-assisted intent reconstruction

Replace or complement deterministic extraction with model-assisted interpretation.

### 🔗 External system integration

Connect field context and decision processing to operational APIs and enterprise systems.

### 🔄 Extended feedback processing

Develop richer feedback histories, correction scopes and decision trace mechanisms.

### 🧠 Context evolution

Expand context handling across multiple interactions and operational workflows.

### 📊 Advanced visualization

Introduce additional graph views for dependencies, transitions and feedback relationships.

These are architectural extension directions, not claims of currently implemented functionality.

---

# 🎯 What RICO-7 Demonstrates

RICO-7 demonstrates a development workflow in which the system is reconstructed before implementation begins.

The initial problem is translated into:

1. A relational architecture
2. Shared technical components
3. Explicit interfaces and states
4. Three executable developer tools
5. An inspectable visual representation
6. A documented engineering handover

The central engineering achievement is the relationship between these elements.

**Three tools. One architectural foundation.**

The system can be studied, executed and extended without treating each module as an unrelated application.

---

# 🧭 The Larger Question

## What should an AI hackathon actually optimize?

Code generation is becoming increasingly accessible.

The challenge is no longer limited to producing source files quickly.

It also involves determining:

- What system should exist?
- Which relationships must it preserve?
- How should decisions and feedback interact?
- Where are its architectural boundaries?
- How can coherence be examined before implementation?
- How can additional capabilities be integrated without fragmenting the system?

RICO-7 was developed as a practical exploration of these questions.

Its engineering sequence was deliberate:

**Understand the system. Design the architecture. Examine coherence. Implement. Verify.**

---

# 🔐 Intellectual Property & Usage

Copyright © 2026 Ottavio Braun.

All rights reserved.

RICO-7 and its associated SYNTX architectural materials are proprietary.

The availability of source code or documentation does not itself grant permission to reproduce, distribute, modify, commercialize or incorporate the materials into another product.

Any use beyond authorized evaluation requires prior written permission from the rights holder.

Existing contractual obligations and applicable law remain unaffected.

---

# ✍️ Author

**Ottavio Braun**  
Strategic System Architect  
Creator of SYNTX

🌐 https://www.syntx-system.com

---

## 🧬 SYNTX

**Relations before isolated entities.**

**Architecture before code.**

**Coherence before implementation.**

**Build systems, not disconnected features.**
