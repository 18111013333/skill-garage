**Examples**:
```bash
# Default: 20 attempts, 5s intervals
python3 scripts/ai_picture_book_poll.py "task-id-here"

# Custom: 30 attempts, 10s intervals
python3 scripts/ai_picture_book_poll.py "task-id-here" 30 10
```

### Manual Polling
1. Create task → store `task_id`
2. Query every 5-10s until status = 2
3. Timeout after 2-3 minutes

## Error Handling

- Invalid content: "Content cannot be empty"
- Invalid type: "Invalid type. Use 9 (static) or 10 (dynamic)"
- Processing error: "Failed to generate picture book"
- Timeout: "Task timed out. Try again later"
