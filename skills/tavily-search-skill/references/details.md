
## Usage

### Basic Search

```bash
./search.sh "search query"
```

### Specify Result Count

```bash
./search.sh "query" 10
```

### Include Images

```bash
./search.sh "query" 5 true
```

## Dependencies

- `curl`
- `jq`

Install if missing:
- Ubuntu/Debian: `sudo apt-get install curl jq`
- macOS: `brew install curl jq`
- Alpine: `apk add curl jq`
