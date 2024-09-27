from datetime import datetime, timedelta
from rgbmatrix import graphics
from PIL import Image
from data import MlbGame
from models.mlb import GameState
from models.mlb.attributes import InningState
from scenes.scene import Scene
from utils.colors import text_color_yellow, light_green, light_red, text_color_red


class MlbGameScene(Scene):
    name = 'mlb'
    _refresh_pregame_delay = timedelta(minutes=30)
    _refresh_in_progress_delay = timedelta(seconds=30)

    def __init__(self, canvas, team, date_arg):
        super().__init__(canvas)

        game_date = datetime.now() if date_arg is None else date_arg

        self._mlb_game = MlbGame(team)
        self._mlb_game.get_game(game_date)
        self._home_logo = Image.open(f'resources/images/mlb/{self._mlb_game.home_team.team_id}.png').convert('RGB')
        self._away_logo = Image.open(f'resources/images/mlb/{self._mlb_game.away_team.team_id}.png').convert('RGB')

    def _check_if_refresh_required(self) -> bool:
        if self._prev_refresh_time is None:
            return True
        elif self._mlb_game.game_state == GameState.PREGAME:
            return self._now - self._prev_refresh_time >= self._get_pregame_refresh_delay()
        elif self._mlb_game.game_state == GameState.FINAL:
            return False
        elif self._mlb_game.game_state == GameState.IN_PROGRESS:
            return self._now - self._prev_refresh_time >= self._refresh_in_progress_delay

    def _refresh_data(self):
        print(f'Refreshing game data - {self._now}')
        self._mlb_game.refresh_game()

    def display(self):
        print('Re-drawing mlb scene')
        self._canvas.draw_image(2, 2, self._away_logo)
        self._canvas.draw_image(46, 2, self._home_logo)

        if self._mlb_game.game_state == GameState.PREGAME or self._mlb_game.game_state == GameState.SCHEDULED:
            # Draw game state/current inning
            start_time = self._mlb_game.start_time
            if start_time:
                start_time_pos_x = 19 if len(start_time) == len('00:00am') else 21
                self._canvas.draw_text_xs(start_time_pos_x, 21, start_time, text_color_yellow)
            if self._mlb_game.game_time is not None:
                month_day_pos_y = 10
                if self._mlb_game.game_time.year != self._now.year:
                    month_day_pos_y = 7
                    self._canvas.draw_text_xs(25, 14, self._mlb_game.game_time.strftime('%Y'), text_color_yellow)
                self._draw_month_day(24, month_day_pos_y, text_color_yellow)

            # Draw win/loss record
            away_record = f'{self._mlb_game.away_team.wins}-{self._mlb_game.away_team.losses}'
            away_record_x = 1
            if len(away_record) == 4:
                away_record_x = 2
            elif len(away_record) == 3:
                away_record_x = 4

            home_record = f'{self._mlb_game.home_team.wins}-{self._mlb_game.home_team.losses}'
            home_record_x = 44
            if len(home_record) == 4:
                home_record_x = 47
            elif len(home_record) == 3:
                home_record_x = 49

            self._canvas.draw_text_xs(away_record_x, 30, away_record, text_color_yellow)
            self._canvas.draw_text_xs(home_record_x, 30, home_record, text_color_yellow)
        else:
            # Draw runs
            home_run_color = text_color_yellow
            away_run_color = text_color_yellow
            if self._mlb_game.game_state == GameState.FINAL and self._mlb_game.home_team.runs != self._mlb_game.away_team.runs:
                home_team_wins = self._mlb_game.home_team.runs > self._mlb_game.away_team.runs
                home_run_color = light_green if home_team_wins else light_red
                away_run_color = light_red if home_team_wins else light_green
            away_runs_pos_x = 6
            if self._mlb_game.away_team.runs >= 10:
                away_runs_pos_x = 2
            self._canvas.draw_text_md_bold(away_runs_pos_x, 30, f'{self._mlb_game.away_team.runs}', away_run_color)
            home_runs_pos_x = 51
            if self._mlb_game.home_team.runs >= 10:
                home_runs_pos_x = 47
            self._canvas.draw_text_md_bold(home_runs_pos_x, 30, f'{self._mlb_game.home_team.runs}', home_run_color)

        if self._mlb_game.game_state == GameState.IN_PROGRESS or self._mlb_game.game_state == GameState.SUSPENDED:
            # Draw current inning
            if self._mlb_game.inning_text:
                inning_text_pos_x = 20
                inning_state_len = self._canvas.draw_text_xs(inning_text_pos_x, 7, self._mlb_game.inning_state.string, text_color_yellow)
                self._canvas.draw_text_xs(inning_text_pos_x + inning_state_len + 2, 7, self._mlb_game.inning_text, text_color_yellow)

            # Draw possession arrow
            if self._mlb_game.inning_state != InningState.MIDDLE and self._mlb_game.inning_state != InningState.END:
                if self._mlb_game.is_top_of_inning:
                    self._canvas.draw_text_sm(18, 18, '<', text_color_yellow)
                else:
                    self._canvas.draw_text_sm(40, 18, '>', text_color_yellow)

            # Draw on-base runners
            first_pos_x = 33
            first_pos_y = 12
            self._canvas.draw_diamond(first_pos_x, first_pos_y, 3, text_color_yellow)
            if self._mlb_game.is_on_first:
                self._fill_in_base(first_pos_x, first_pos_y, text_color_yellow)

            second_pos_x = 29
            second_pos_y = 8
            self._canvas.draw_diamond(second_pos_x, second_pos_y, 3, text_color_yellow)
            if self._mlb_game.is_on_second:
                self._fill_in_base(second_pos_x, second_pos_y, text_color_yellow)

            third_pos_x = 25
            third_pos_y = 12
            self._canvas.draw_diamond(third_pos_x, third_pos_y, 3, text_color_yellow)
            if self._mlb_game.is_on_third:
                self._fill_in_base(third_pos_x, third_pos_y, text_color_yellow)

            # Draw ball/strike count
            print(f'Current strikes: {self._mlb_game.strikes}')
            self._canvas.draw_text_sm(24, 25, f'{self._mlb_game.balls}', text_color_yellow)
            self._canvas.draw_line(30, 22, 32, 22, text_color_yellow)
            self._canvas.draw_text_sm(35, 25, f'{self._mlb_game.strikes}', text_color_yellow)

            # Draw outs
            self._canvas.draw_circle(21, 28, 2, text_color_yellow)
            self._canvas.draw_circle(31, 28, 2, text_color_yellow)
            self._canvas.draw_circle(41, 28, 2, text_color_yellow)
            if self._mlb_game.outs > 0:
                # self._canvas.draw_circle(21, 28, 1, text_color_yellow)
                self._fill_in_out(21, 28, text_color_yellow)
            if self._mlb_game.outs > 1:
                # self._canvas.draw_circle(31, 28, 1, text_color_yellow)
                self._fill_in_out(31, 28, text_color_yellow)
            if self._mlb_game.outs > 2:
                # self._canvas.draw_circle(41, 28, 1, text_color_yellow)
                self._fill_in_out(41, 28, text_color_yellow)

        elif self._mlb_game.game_state == GameState.FINAL:
            # Draw Final text and date if not today
            self._canvas.draw_text_sm(20, 14, GameState.FINAL.string, text_color_yellow)
            if self._mlb_game.game_time and self._mlb_game.game_time.date() != self._now.date():
                self._draw_month_day(24, 22, text_color_yellow)
                if self._mlb_game.game_time.year != self._now.year:
                    self._canvas.draw_text_xs(25, 29, self._mlb_game.game_time.strftime('%Y'), text_color_yellow)

    def _refresh_display_required(self) -> bool:
        # We only want to refresh the display when the data changes
        return False

    def _compare_start_time(self):
        if self._mlb_game is not None and self._mlb_game.game_time is not None:
            return self._now.astimezone() + self._refresh_pregame_delay >= self._mlb_game.game_time
        return False

    def _get_pregame_refresh_delay(self) -> timedelta:
        if self._compare_start_time():
            return timedelta(minutes=1)
        return self._refresh_pregame_delay

    def _fill_in_base(self, x: int, y: int, color: graphics.Color):
        self._canvas.draw_line(x + 1, y + 2, x + 3, y + 2, color)
        self._canvas.draw_line(x + 2, y + 1, x + 2, y + 3, color)

    def _fill_in_out(self, x: int, y: int, color: graphics.Color):
        self._canvas.draw_line(x - 1, y - 1, x + 1, y - 1, color)
        self._canvas.draw_line(x - 1, y, x + 1, y, color)
        self._canvas.draw_line(x - 1, y + 1, x + 1, y + 1, color)

    def _draw_month_day(self, x: int, y: int, color: graphics.Color):
        if self._mlb_game.game_time is not None:
            month = self._mlb_game.game_time.strftime('%b')
            day = str(int(self._mlb_game.game_time.strftime('%d')))
            day_pos_x = x
            if len(day) > 1:
                day_pos_x = x - 2
            month_len = self._canvas.draw_text_xs(day_pos_x, y, month, color)
            self._canvas.draw_text_xs(day_pos_x + month_len + 2, y, day, color)
