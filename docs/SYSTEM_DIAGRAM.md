# System diagram — A2

Legend: **[I] implemented**, **[S] simulated**, **[P] planned**. The UI and HTTP handler are real; the response *content* is simulated. No LLM is connected.

```mermaid
flowchart TD
  A[User: day-trip goal] --> B[Chat page / text input — I]
  B -->|POST /api/chat: message| C[Local HTTP server — I]
  C --> D[Rule-based intent extractor — I]
  D --> E{Activity clear? — I}
  E -->|Yes| F[Sample itinerary generator — S]
  E -->|No| G[Warning: interpretation is an assumption — I]
  G --> F
  F --> H[On-screen reply and feedback — I]
  H --> J{Refine request? — I}
  J -->|No| A
  J -->|Yes| K[Activity / budget / distance controls — I]
  K -->|POST /api/refine: selected constraints| L[Validate and merge intent — I]
  L --> F
  L --> M[Optional external LLM / real map data — P]
```

**Data and control flows:** The browser sends JSON messages to `/api/chat`. The server parses text via regular expressions, returns intent metadata, an ambiguity flag and a deterministic illustrative answer. The browser shows a correction affordance. When selected, the browser sends structured options to `/api/refine`; the server validates them and regenerates the sample answer. All requests are local and stateless. The optional LLM / external data are not called.
