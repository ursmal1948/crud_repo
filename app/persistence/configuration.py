from app.persistence.repository import TeamRepository, PlayerRepository
from app.persistence.connection import connection_pool
from app.service.players_with_teams import PlayersWithTeamsService

team_repo = TeamRepository(connection_pool)
player_repo = PlayerRepository(connection_pool)
players_with_teams_service = PlayersWithTeamsService(player_repo, team_repo)
