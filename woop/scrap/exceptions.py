class WoopError(Exception):
    """Erreur générale WOOP"""
    pass


class WoopConnectionError(WoopError):
    """Erreur de connexion"""
    pass