#!/usr/bin/env python3
"""Migration script to canonicalize `object_type` values in data/objects.csv.

This script makes a backup of the original CSV before writing changes.

Usage:
    python scripts/migrate_object_types.py
"""
import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd
from utils.data_handler import DataHandler


def main():
    handler = DataHandler()
    src = handler.objects_file
    if not src.exists():
        print(f"No objects file found at {src}")
        return

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = src.parent / f"objects.csv.bak-{ts}"
    shutil.copy2(src, backup)
    print(f"Backup created: {backup}")

    df = pd.read_csv(src)
    if "object_type" not in df.columns:
        print("No object_type column found; nothing to migrate.")
        return

    before_values = df["object_type"].astype(str).unique().tolist()
    df = df.copy()
    df["object_type"] = df["object_type"].apply(handler.normalize_object_type)
    after_values = df["object_type"].astype(str).unique().tolist()

    # Write using handler's atomic writer
    handler._write_df_atomic(src, df)

    changed = set(before_values) - set(after_values)
    print("Migration complete.")
    print(f"Unique values before: {before_values}")
    print(f"Unique values after:  {after_values}")
    if changed:
        print(f"Values normalized (removed): {list(changed)}")
    else:
        print("No values were changed.")


if __name__ == "__main__":
    main()
