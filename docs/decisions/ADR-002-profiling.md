# ADR-002: Use Pandas + NumPy for Data Profiling

## Status
Accepted

## Date
2026-02-05

## Context
We need to automatically profile uploaded datasets to extract:
- Schema metadata (column names, types, nullability)
- Statistical profile (row count, cardinality, min/max, mean/std)
- Quality metrics (null %, duplicate rate, uniqueness)
- Semantic tags (PII detection, temporal columns)

## Options Considered

### Option 1: Pandas + NumPy
**Pros:**
- Industry standard for data manipulation
- Rich profiling capabilities
- Excellent documentation
- JD requirement alignment
- Works with CSV, Parquet, JSON

**Cons:**
- Memory-bound for very large datasets
- Single-threaded by default

### Option 2: Polars
**Pros:**
- Faster than Pandas
- Better memory efficiency
- Rust-based parallelism

**Cons:**
- Smaller ecosystem
- Not a JD requirement
- API differences from Pandas

### Option 3: Great Expectations
**Pros:**
- Purpose-built for data quality
- Rich validation rules

**Cons:**
- Heavier dependency
- Overkill for profiling only
- Learning curve

## Decision
**Pandas + NumPy** - Industry standard, aligns with JD requirements, sufficient for demo scale (100K-500K rows).

## Consequences
- Profile datasets up to ~1M rows in memory
- Use chunked processing for larger files if needed
- Leverage NumPy for vectorized statistics
- Consider Polars migration path for production scale

## Implementation Notes
```python
# Example profiling approach
profile = {
    "row_count": len(df),
    "columns": [
        {
            "name": col,
            "dtype": str(df[col].dtype),
            "null_pct": df[col].isnull().mean(),
            "cardinality": df[col].nunique(),
            "stats": df[col].describe().to_dict() if pd.api.types.is_numeric_dtype(df[col]) else None
        }
        for col in df.columns
    ]
}
```
