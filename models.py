from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BotConfig(BaseModel):
    """
    Représente la configuration d'un bot stockée en base de données.
    """
    id: str = Field(..., description="Identifiant unique du bot (UUID)")
    name: str = Field(..., description="Nom d'affichage du bot")
    path: str = Field(..., description="Chemin local vers les fichiers du bot")
    language: str = Field(..., description="python ou nodejs")
    entry_point: str = Field(..., description="Fichier principal à lancer")
    auto_restart: bool = Field(default=True, description="Redémarrer si le bot crash")
    created_at: datetime = Field(default_factory=datetime.now)

class BotStatus(BaseModel):
    """
    Représente l'état en temps réel d'un bot pour l'interface web.
    """
    bot_id: str
    is_running: bool
    uptime: Optional[str] = None
    memory_usage: Optional[float] = Field(0, description="Utilisation RAM en Mo")
    cpu_usage: Optional[float] = Field(0, description="Pourcentage CPU")
    last_error: Optional[str] = None

class BotCreate(BaseModel):
    """
    Schéma utilisé pour la création d'un nouveau bot via l'API.
    """
    name: str
    zip_url: Optional[str] = None # Pour les imports futurs
