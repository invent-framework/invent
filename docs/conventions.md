---
icon: lucide/braces
---

# Naming Conventions

## Min/Max Property Names

Invent uses explicit min/max naming for all bounded values.

Use:

- `min_value`
- `max_value`

For bounded text length values, use:

- `min_length`
- `max_length`

Examples:

```python
Slider(min_value=0, max_value=100)
Rating(max_value="5")
TextInput(min_length=3, max_length=20)
```

This naming keeps APIs predictable by making both the bound and the bounded
thing explicit.
