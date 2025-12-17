# This function normalizes country names by converting them to lowercase
# and replacing accented characters with their unaccented counterparts.
# Avoid silent errors 

def normalize_country(name: str) -> str:
    return (
        name.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .strip()
    )
