from dataclasses import dataclass
from app.persistence.model import Player, Team
from app.persistence.repository import PlayerRepository, TeamRepository
from app.service.dto import CreatePlayerWithTeamDto
from dataclasses import dataclass


@dataclass
class PlayersWithTeamsService:
    player_repository: PlayerRepository
    team_repository: TeamRepository

    def add_player_with_team(self, create_player_with_team_dto: CreatePlayerWithTeamDto):
        team_from_db = self.team_repository.find_by_name(create_player_with_team_dto.team_name)
        if not team_from_db:
            raise ValueError('Team not found')
        player = Player(
            name=create_player_with_team_dto.player_name,
            goals=create_player_with_team_dto.player_goals,
            team_id=team_from_db.id_
        )
        return self.player_repository.insert(player)

    def transfer_players_with_goals_higher_than_to_the_team(self, goal_limit: int, team: Team):
        team_from_db = self.team_repository.find_by_name(team.name)
        if not team_from_db:
            raise ValueError('Team not found')

        players_to_be_transfered = self.player_repository.find_all_with_goals_higher_than(goal_limit)
        return [self.player_repository.update(player.id_, Player(goals=player.goals, team_id=team_from_db.id_)) for
                player in players_to_be_transfered]
        # return [self.player_repository.change_player_team(player, team_from_db) for player in players_to_be_transfered]

    # def change_player_team(self, player: Player, team: Team):
    #     new_team_id = team.id_
    #     return self.update(player.id_, Player(goals=player.goals, team_id=new_team_id))
