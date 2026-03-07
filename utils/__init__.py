# Utils module for mymaintlog application

import pandas as pd


def selectbox_label(record_id, df, id_col, name_col=None, desc_col=None):
    """Return 'id - name' for selectboxes; fall back to first 4 words of description."""
    rows = df[df[id_col] == record_id]
    if rows.empty:
        return str(record_id)
    row = rows.iloc[0]
    if name_col:
        name = str(row.get(name_col, '') or '').strip()
        if name:
            return f"{record_id} - {name}"
    if desc_col:
        desc = str(row.get(desc_col, '') or '').strip()
        words = ' '.join(desc.split()[:4])
        if words:
            return f"{record_id} - {words}"
    return str(record_id)
