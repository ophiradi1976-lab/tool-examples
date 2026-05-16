# plantuml — Diagram Generation from Text

Generates diagrams (sequence, class, component, ER, activity, etc.) from
plain-text `.puml` files. Graphviz is installed alongside it for graph layouts.

## Basic usage

```bash
plantuml diagram.puml                   # generate PNG (default)
plantuml -tsvg diagram.puml            # generate SVG
plantuml -tpdf diagram.puml            # generate PDF
plantuml -o output/ diagram.puml       # output to a specific directory
plantuml *.puml                         # batch process all .puml files
```

## Diagram types

### Sequence diagram

```plantuml
@startuml
Client -> Server: HTTP GET /api/data
Server -> DB: SELECT * FROM items
DB --> Server: rows
Server --> Client: 200 OK [JSON]
@enduml
```

### Class diagram

```plantuml
@startuml
class User {
  +id: int
  +email: string
  +login(): bool
}
class Order {
  +userId: int
  +total: float
}
User "1" --> "*" Order
@enduml
```

### Component / architecture diagram

```plantuml
@startuml
package "Backend" {
  [API Gateway]
  [Auth Service]
  [Order Service]
}
database "PostgreSQL"
[API Gateway] --> [Auth Service]
[API Gateway] --> [Order Service]
[Order Service] --> PostgreSQL
@enduml
```

### Activity / flowchart

```plantuml
@startuml
start
:Receive request;
if (Authenticated?) then (yes)
  :Process request;
  :Return 200;
else (no)
  :Return 401;
endif
stop
@enduml
```

### ER diagram

```plantuml
@startuml
entity "User" {
  *id : int
  --
  email : varchar
  created_at : timestamp
}
entity "Order" {
  *id : int
  --
  user_id : int <<FK>>
  total : decimal
}
User ||--o{ Order
@enduml
```

## Flags

| Flag | Meaning |
|------|---------|
| `-tpng` | PNG output (default) |
| `-tsvg` | SVG output (scalable, good for docs) |
| `-tpdf` | PDF output |
| `-o dir` | Output directory |
| `-charset UTF-8` | Explicit charset |
| `-checkonly` | Validate syntax without generating |
| `-language` | Print all keywords |

## Neovim integration

With the playbook's Neovim config, `.puml` files may render previews via a
plugin like `weirongxu/plantuml-previewer.vim`.

## Use-cases

- Architecture diagrams in project docs (committed as `.puml`, rendered to SVG)
- Sequence diagrams for API documentation
- ER diagrams generated from schema
- Keeping diagrams in version control alongside code (text = diffable)
