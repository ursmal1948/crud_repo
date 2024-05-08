from app.persistence.model import Team, Player
from app.service.players_with_teams import PlayersWithTeamsService
from app.service.dto import CreatePlayerWithTeamDto
from app.persistence.connection import connection_pool
from app.persistence.configuration import player_repo, team_repo
from app.persistence.repository import PlayerWithTeamRepository


def main() -> None:
    players_with_teams_service = PlayersWithTeamsService(player_repo, team_repo)
    # player_repo.update(1, Player(team_id=1,goals=20))
    # players_with_teams_service.add_player_with_team(CreatePlayerWithTeamDto(
    #     player_name='SB ELSE',
    #     player_goals=300,
    #     team_name='AA'
    # ))
    # woiecej niz 40 do b
    # players_with_teams_service.transfer_players_with_goals_higher_than_to_the_team(1000, 'AA')
    # players_with_teams_service.transfer_players_with_goals_higher_than_to_the_team()
    # print(team_repo.find_all())
    # team = Team(id_=4, name='CC', points=50)  # 150 do team 1
    # print(players_with_teams_service.transfer_players_with_goals_higher_than_to_the_team(220, team))
    print(player_repo.find_all_meeting_regex('^[A-Z][a-z]+ [1-9][0-9]*$'))
    # pl_with_team_repo = PlayerWithTeamRepository(connection_pool)
    # print(pl_with_team_repo.find_all_players_with_teams(14, 45))
    # print(inflection.tableize("Stadion"))
    # print(CrudRepository(connection_pool,Stadium)._table_name())
    # print(crud_repo.delete(6))
    # print(crud_repo.count())
    # crud_repo.insert(Team(1, 'A', 10))
    # crud_repo.insert(Team(3, 'C', 40))
    # crud_repo.insert(Player(1, 'Player 1', 20, 1))
    # crud_repo.insert(Player(name='Player 3', goals=50, team_id=3))
    # player_repo.update(1, Player(goals=200, team_id=2))
    # crud_repo.update(1, Team(name='AA', points=100))
    # with connection_pool.get_connection() as conn:
    #     cursor = conn.cursor()
    #     #
    #     teams_table_sql = '''
    #         create table if not exists teams (
    #             id_ integer primary  key auto_increment,
    #             name varchar(50) not null,
    #             points integer default 0
    #             )
    #         '''
    #     players_table_sql = '''
    #           create table if not exists players (
    #               id_ integer primary key auto_increment,
    #               name varchar(50) not null,
    #               goals integer default 0,
    #               team_id integer,
    #               foreign key (team_id) references teams(id_) on delete cascade on update cascade
    #                   );
    #                '''
    #     # cursor.execute(teams_table_sql)
    #     cursor.execute(players_table_sql)
    #     # cursor.execute('show tables;')
    #     print(cursor.fetchall())

    # with connection_pool.get_connection() as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("insert into teams (name, points) values ('B',30)")
    #     # cursor.execute("insert into teams (name, points) values (10,20,30)")
    #     conn.commit()


if __name__ == '__main__':
    main()
