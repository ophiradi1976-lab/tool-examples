# jq — JSON Processor

A lightweight command-line JSON processor. Filter, transform, and query JSON
from APIs, files, and pipelines.

## Basic usage

```bash
jq '.' file.json                   # pretty-print JSON
cat file.json | jq '.'             # pipe from stdin
curl -s https://api.example.com | jq '.'
```

## Field access

```bash
jq '.name' file.json               # top-level field
jq '.address.city' file.json       # nested field
jq '.items[0]' file.json           # first array element
jq '.items[-1]' file.json          # last element
jq '.items[2:5]' file.json         # slice
```

## Array operations

```bash
jq '.[]' file.json                 # iterate array elements
jq '.[] | .name' file.json         # pluck a field from each element
jq 'length' file.json              # length of array or string
jq 'keys' file.json                # keys of an object
```

## Filters and select

```bash
jq '.[] | select(.active == true)' file.json
jq '.[] | select(.age > 30)' file.json
jq '.[] | select(.name | startswith("A"))' file.json
```

## Transforming / building output

```bash
# Build a new object
jq '.[] | {id: .id, label: .name}' file.json

# Create an array from results
jq '[.[] | .name]' file.json

# Extract multiple fields as CSV
jq -r '.[] | [.id, .name, .email] | @csv' file.json

# TSV output
jq -r '.[] | [.id, .name] | @tsv' file.json
```

## Useful flags

```bash
jq -r '...'       # raw output (no quotes around strings)
jq -c '...'       # compact output (single line)
jq -s '...'       # slurp: read all input into an array
jq -e '...'       # exit non-zero if result is false/null
jq -n '...'       # no input (use for constructing JSON)
```

## Common real-world patterns

```bash
# Get all keys in a JSON object
jq 'keys' config.json

# Count items in an array
jq '.items | length' response.json

# Filter AWS CLI output
aws ec2 describe-instances | jq '.Reservations[].Instances[] | {id: .InstanceId, state: .State.Name}'

# Extract values from GitHub API
curl -s https://api.github.com/users/eddiegold/repos | jq '.[].name'

# Pretty-print and filter a log stream
tail -f app.log | jq 'select(.level == "error")'

# Merge two JSON objects
jq -n --argjson a '{"x":1}' --argjson b '{"y":2}' '$a + $b'
```
