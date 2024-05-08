from app.persistence.repository import TeamRepository, PlayerRepository
from app.persistence.connection import connection_pool

team_repo = TeamRepository(connection_pool)
player_repo = PlayerRepository(connection_pool)
