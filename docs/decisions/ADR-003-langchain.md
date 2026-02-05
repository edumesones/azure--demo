# ADR-003: Use LangChain for RAG Pipeline

## Status
Accepted

## Date
2026-02-05

## Context
We need a framework to build the RAG (Retrieval-Augmented Generation) pipeline for natural language queries over metadata.

Requirements:
- Query understanding and intent classification
- Hybrid search (vector + keyword)
- Context augmentation with retrieved metadata
- LLM response generation with citations
- Conversation memory for multi-turn

## Options Considered

### Option 1: LangChain
**Pros:**
- Mature ecosystem with extensive documentation
- Modular chain composition
- Built-in integrations (OpenAI, ChromaDB, etc.)
- LangSmith for observability
- JD requirement alignment
- Active development and community

**Cons:**
- Can be verbose for simple use cases
- Frequent breaking changes (mitigated with version pinning)

### Option 2: LlamaIndex
**Pros:**
- Purpose-built for RAG
- Good for document indexing

**Cons:**
- Less flexible for custom chains
- Smaller ecosystem
- Not a JD requirement

### Option 3: Custom Implementation
**Pros:**
- Full control
- No framework overhead

**Cons:**
- More development time
- Reinventing the wheel
- No observability tooling

## Decision
**LangChain** - Mature ecosystem, JD alignment, excellent RAG support with LangSmith observability.

## Consequences
- Use LCEL (LangChain Expression Language) for chain composition
- Integrate LangSmith for tracing and debugging
- Pin langchain version to avoid breaking changes
- Structure chains by query intent (discovery, quality, lineage)

## Implementation Pattern
```python
# Chain structure
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```
