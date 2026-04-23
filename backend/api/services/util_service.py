# Internal
import os
import locale

try:
    for env_var in ["LC_ALL", "LANG"]:
        if env_var not in os.environ:
            os.environ[env_var] = "C.UTF-8"
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass


def format_currency(value):
    """Format number as Spanish currency"""
    if value is None:
        return "0,00 €"
    try:
        num = float(value)
        formatted = locale.format_string("%.2f", num, grouping=True)
        return f"{formatted} €"
    except (ValueError, TypeError):
        return f"{value} €"


def get_raw_value(value):
    """Extract numeric value from possibly formatted string"""

    if value is None:
        return 0

    if isinstance(value, (int, float)):
        return float(value)

    if hasattr(value, "quantize"):
        return float(value)

    if isinstance(value, str):
        clean = value.replace("€", "").replace(" ", "").strip()
        clean = clean.replace(".", "").replace(",", ".")

        try:
            return float(clean)
        except ValueError:
            return 0

    return 0
