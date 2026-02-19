# Optimized Dataset Schema

This folder contains a consolidated, context-efficient version of all 87 Corva dataset schemas.

## Files

- `datasets.yaml` - Single consolidated schema file (~650 lines vs ~8,700 lines original)

## Format

### Type Abbreviations

| Abbrev | Type |
|--------|------|
| `f` | float |
| `i` | int |
| `l` | long |
| `s` | string |
| `o` | object |
| `a` | array |
| `b` | boolean |

### Templates

Common patterns are defined once as templates:
- `base` - Standard keys (timestamp, asset_id) and fields (company_id)
- `summary` - Aggregated data with min/max/mean/median
- `stage_based` - Completion data keyed by stage_number
- `activity_summary` - Activity breakdown arrays

Datasets use `inherits: template_name` to avoid repetition.

### Structure

```yaml
datasets:
  dataset_name:
    collection: actual.collection.name
    desc: Brief description
    freq: update_frequency
    inherits: template_name  # optional
    keys: [primary, keys]    # if different from template
    fields:
      field.name: type
```

## Context Efficiency

| Version | Lines | Est. Tokens |
|---------|-------|-------------|
| Original (87 files) | ~8,700 | ~65,000 |
| Optimized (1 file) | ~650 | ~8,000 |
| **Savings** | **92%** | **88%** |

## Usage

Load this single file instead of all 87 markdown files to reduce context consumption by ~57,000 tokens while retaining all schema information needed for:
- Field lookups
- Query construction
- Data type validation
- Understanding data relationships

## What's Preserved

- All 87 dataset definitions
- Collection names
- Primary keys
- Field names and types
- Update frequencies
- Brief descriptions
