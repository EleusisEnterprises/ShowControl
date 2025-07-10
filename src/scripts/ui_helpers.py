from typing import List, Union


def _get_op(op_or_path):
    """Return the operator object from a path or object."""
    return op(op_or_path) if isinstance(op_or_path, str) else op_or_path


def get_selected_layer(dropdown):
    """Return the selected label from a Dropdown COMP used for layer selection."""
    dd = _get_op(dropdown)
    if dd is None:
        return ""
    if hasattr(dd, 'panel') and hasattr(dd.panel, 'label'):
        return dd.panel.label
    if hasattr(dd.par, 'value0'):
        return str(dd.par.value0.eval())
    if hasattr(dd.par, 'value'):
        return str(dd.par.value.eval())
    return ""


def get_numeric_value(field):
    """Return the numeric value from a field COMP or Parameter."""
    fld = _get_op(field)
    if fld is None:
        return 0
    if hasattr(fld, 'val'):
        try:
            return float(fld.val)
        except Exception:
            return 0
    if hasattr(fld.par, 'value0'):
        return float(fld.par.value0.eval())
    if hasattr(fld.par, 'value'):
        return float(fld.par.value.eval())
    return 0


def build_osc_address(parts: List[str]) -> str:
    """Return a sanitized OSC address assembled from the given parts."""
    clean = [str(p).strip('/') for p in parts if p not in (None, '')]
    return '/' + '/'.join(clean)


def assemble_osc_address(layer_dd, channel_dd, index_field=None) -> str:
    """Build an OSC address like `/layer/channel/index` from UI selections."""
    parts = [
        get_selected_layer(layer_dd),
        get_selected_layer(channel_dd),
    ]
    if index_field is not None:
        parts.append(str(int(get_numeric_value(index_field))))
    return build_osc_address(parts)
')