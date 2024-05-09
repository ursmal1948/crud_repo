from app.persistence.model import Player, Team
from app.persistence.repository import PlayerRepository, TeamRepository
from app.service.dto import CreatePlayerWithTeamDto
from dataclasses import dataclass
from collections import defaultdict, Counter
from typing import Callable


@dataclass
class PlayersService:
    player_repository: PlayerRepository

    def add_goals(self, player_id: int, goald_to_add: int):
        player_from_db = self.player_repository.find_by_id(player_id)
        if not player_from_db:
            raise ValueError('Player not found')
        return self.player_repository.update(player_id, Player(goals=player_from_db.goals + goald_to_add))

    def change_player_name(self, player_id: int, new_name: str):
        player_from_db = self.player_repository.find_by_id(player_id)
        if not player_from_db:
            raise ValueError('Player not found')
        return self.player_repository.update(player_id, Player(name=new_name))


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

    # po id ? czy przekazywanie instancji.
    def change_player_team(self, player: Player, team: Team):
        new_team = self.team_repository.find_by_id(team.id_)
        if not new_team:
            raise ValueError('Team not found')
        return self.player_repository.update(player.id_, Player(team_id=new_team.id_))

    def remove_player_from_team(self, player_id: int):
        player = self.player_repository.find_by_id(player_id)
        if not player:
            raise ValueError('Player not found')
        return self.player_repository.delete(player_id)

    def transfer_players_with_goals_higher_than_to_the_team(self, goal_limit: int, team: Team):
        team_from_db = self.team_repository.find_by_name(team.name)
        if not team_from_db:
            raise ValueError('Team not found')

        players_to_be_transfered = self.player_repository.find_all_with_goals_higher_than(goal_limit)
        return [self.player_repository.update(player.id_, Player(team_id=team_from_db.id_)) for
                player in players_to_be_transfered]

    def get_team_ids_with_extreme_goals(self, extreme_fn: Callable[[list[int]], int]):
        teams_from_db = self.team_repository.find_all()
        grouped_by_goals = defaultdict(list)
        for team in teams_from_db:
            goals = self.team_repository.calculate_total_goals_for_team(team.id_)
            if goals is not None:
                grouped_by_goals[goals].append(team.id_)
        print(f"GOALS:{dict(grouped_by_goals)}")
        extreme_value = extreme_fn(list(grouped_by_goals.keys()))
        return grouped_by_goals[extreme_value]

    def group_teams_by_players_count(self):
        team_players_count = self.team_repository.get_team_player_counts()
        grouped_by_players_count = Counter()
        for team, count in team_players_count:
            grouped_by_players_count[team] = count
        return dict(grouped_by_players_count)

    def calculate_average_goals_per_team(self):
        team_players_count = self.team_repository.get_team_player_counts()  # ('A', 3), ('B', 4)
        grouped_by_goals = defaultdict(int)
        for team_name, players_count in team_players_count:
            print(players_count)
            team_id = self.team_repository.get_team_id_by_name(team_name)
            total_goals_for_team = self.team_repository.calculate_total_goals_for_team(team_id)
            if total_goals_for_team and players_count:
                grouped_by_goals[team_id] = total_goals_for_team // players_count
        return dict(grouped_by_goals)
