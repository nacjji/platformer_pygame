import pygame
from ..constants import *
from ..actions.movement import Movement
from ..objects.platform import Platform  # Platform 클래스 임포트 추가


class Player:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y  # 실제 게임 월드에서의 y 위치
        self.screen_y = y  # 화면상의 y 위치
        self.velocity_y = 0
        self.velocity_x = 0  # x축 속도 추가
        self.is_jumping = False
        self.can_double_jump = False  # 2단 점프 가능 여부
        self.has_double_jumped = False  # 2단 점프 사용 여부
        self.remaining_double_jumps = 0  # 남은 2단 점프 횟수
        self.remaining_jump_boosts = 0  # 남은 점프력 증가 횟수
        self.score = 0  # 현재 점수 (높이)
        self.max_height = 0  # 도달한 최대 높이
        self.is_dead = False
        self.raw_height = 0  # 실제 높이 (배율 적용 전)

        # 버프 효과를 위한 속성
        self.jump_power_multiplier = 1.0  # 점프력 배율
        self.speed_multiplier = 1.0  # 이동속도 배율
        self.is_key_reversed = False  # 키 반전 여부
        self.is_sliding = False  # 슬라이딩 상태
        self.slide_friction = 0.98  # 슬라이딩 마찰력

        # 버프 관리 시스템
        self.active_buffs = set()  # 현재 활성화된 모든 버프
        self.positive_buff = None  # 현재 활성화된 긍정 버프 (연두색, 노란색)
        self.buff_start_height = None  # 버프 적용 시점의 높이

    def set_buff(self, buff_type):
        """현재 활성화된 버프 타입을 설정합니다."""
        # 버프 적용 시점의 높이 저장
        self.buff_start_height = self.raw_height

        # 긍정 버프 (연두색, 노란색) 처리
        if buff_type in ['double_jump', 'jump_boost']:
            if self.positive_buff is None or self.positive_buff == buff_type:
                self.positive_buff = buff_type
                if buff_type == 'double_jump':
                    self.can_double_jump = True
                    self.has_double_jumped = False
                    self.remaining_double_jumps = ITEM_TYPES[buff_type]['duration']
                elif buff_type == 'jump_boost':
                    self.remaining_jump_boosts = ITEM_TYPES[buff_type]['duration']
            return

        # 중첩 가능한 버프 (빨간색, 보라색, 하늘색, 주황색) 처리
        if buff_type in ['key_reverse', 'ice_slide', 'transform']:
            self.active_buffs.add(buff_type)
            if buff_type == 'key_reverse':
                self.is_key_reversed = True
            elif buff_type == 'ice_slide':
                self.is_sliding = True
                self.velocity_x = 0

    def remove_buff(self, buff_type, platforms):
        """특정 버프를 제거합니다."""
        if buff_type == self.positive_buff:
            self.positive_buff = None
            if buff_type == 'double_jump':
                self.can_double_jump = False
                self.has_double_jumped = False
                self.remaining_double_jumps = 0
            elif buff_type == 'jump_boost':
                self.remaining_jump_boosts = 0
                self.jump_power_multiplier = 1.0
        elif buff_type in self.active_buffs:
            self.active_buffs.remove(buff_type)
            if buff_type == 'key_reverse':
                self.is_key_reversed = False
            elif buff_type == 'ice_slide':
                self.is_sliding = False
                self.velocity_x = 0
            elif buff_type == 'transform':
                # transform 발판을 원래 상태로 복구
                for platform in platforms:
                    if platform.is_transformed:
                        platform.revert_to_original()
                        platform.is_transformed = False
                        platform.width = platform.original_width  # 발판 너비 복구

    def remove_all_buffs(self):
        """모든 버프를 제거합니다."""
        self.positive_buff = None
        self.active_buffs.clear()
        self.can_double_jump = False
        self.has_double_jumped = False
        self.remaining_double_jumps = 0
        self.remaining_jump_boosts = 0
        self.jump_power_multiplier = 1.0
        self.speed_multiplier = 1.0
        self.is_key_reversed = False
        self.is_sliding = False
        self.velocity_x = 0

    @property
    def border_color(self):
        """현재 긍정 버프에 따른 테두리 색상을 반환합니다."""
        if self.positive_buff:
            return ITEM_TYPES[self.positive_buff]['color']
        return EXCEL_GRID_COLOR

    @property
    def rect(self):
        """플레이어의 충돌 박스를 반환합니다."""
        return pygame.Rect(
            self.pos_x - PLAYER_WIDTH/2,  # 중심점 기준으로 좌우 위치 계산
            self.pos_y - PLAYER_HEIGHT/2,  # 중심점 기준으로 상하 위치 계산
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )

    @property
    def bottom(self):
        """플레이어의 바닥 y좌표를 반환합니다."""
        return self.pos_y + PLAYER_HEIGHT/2

    @property
    def top(self):
        """플레이어의 상단 y좌표를 반환합니다."""
        return self.pos_y - PLAYER_HEIGHT/2

    def move(self, direction):
        """플레이어를 좌우로 이동시킵니다."""
        # 키가 반전된 경우 방향을 반대로
        if self.is_key_reversed:
            direction = -direction

        if self.is_sliding:
            # 슬라이딩 중에는 속도를 누적
            self.velocity_x += direction * PLAYER_SPEED * self.speed_multiplier * 0.1
            # 최대 속도 제한
            self.velocity_x = max(
                min(self.velocity_x, PLAYER_SPEED * 2), -PLAYER_SPEED * 2)
        else:
            # 일반 이동
            Movement.move_horizontal(self, direction * self.speed_multiplier)

    def jump(self):
        """플레이어가 점프합니다."""
        if not self.is_jumping:
            # 점프력 증가 아이템이 있는 경우
            if self.positive_buff == 'jump_boost' and self.remaining_jump_boosts > 0:
                self.velocity_y = JUMP_POWER * \
                    ITEM_TYPES['jump_boost']['value']
                self.remaining_jump_boosts -= 1
                if self.remaining_jump_boosts <= 0:
                    self.jump_power_multiplier = 1.0
                    self.positive_buff = None
            else:
                self.velocity_y = JUMP_POWER * self.jump_power_multiplier
            self.is_jumping = True
            return True
        elif self.can_double_jump and not self.has_double_jumped and self.remaining_double_jumps > 0:
            self.velocity_y = JUMP_POWER * self.jump_power_multiplier
            self.has_double_jumped = True
            self.remaining_double_jumps -= 1
            if self.remaining_double_jumps <= 0:
                self.can_double_jump = False
            return True
        return False

    def update(self, platforms):
        """플레이어의 상태를 업데이트합니다."""
        Movement.apply_gravity(self, platforms)

        # 발판에 착지했는지 확인
        is_landing = False
        for platform in platforms:
            if platform.is_point_above(self.pos_x, self.bottom):
                is_landing = True
                break

        # 슬라이딩 상태일 때 x축 속도 적용 (발판에 있을 때만)
        if self.is_sliding and is_landing:
            self.pos_x += self.velocity_x
            # 화면 경계 체크
            if self.pos_x < PLAYER_WIDTH/2:
                self.pos_x = PLAYER_WIDTH/2
                self.velocity_x = 0
            elif self.pos_x > SCREEN_WIDTH - PLAYER_WIDTH/2:
                self.pos_x = SCREEN_WIDTH - PLAYER_WIDTH/2
                self.velocity_x = 0
            # 마찰력 적용
            self.velocity_x *= self.slide_friction
        elif self.is_sliding and not is_landing:
            # 공중에서는 슬라이딩 속도를 즉시 0으로 만듦
            self.velocity_x = 0

        # 버프 해제 조건: 상승 10미터 혹은 하강 5미터
        if self.buff_start_height is not None:
            height_change = self.raw_height - self.buff_start_height
            if height_change >= 10 or height_change <= -5:
                for buff_type in list(self.active_buffs):
                    self.remove_buff(buff_type, platforms)
                self.buff_start_height = None

        # 착지 상태가 아니면 점프 불가능
        if not is_landing:
            self.is_jumping = True
        else:
            # 착지했을 때만 점프 상태 초기화
            if self.is_jumping:
                self.is_jumping = False
                self.has_double_jumped = False

        # 화면 아래로 떨어졌는지 확인
        if self.screen_y > SCREEN_HEIGHT + PLAYER_HEIGHT:
            self.is_dead = True

    def draw(self, screen):
        """플레이어와 활성화된 버프들을 화면에 그립니다."""
        # 플레이어 그리기
        pygame.draw.rect(screen, BLACK, (
            int(self.pos_x - PLAYER_WIDTH/2),
            int(self.screen_y - PLAYER_HEIGHT/2),
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        ))

        # 겹겹이 쌓이는 테두리 색상 적용
        border_thickness = 2
        for buff_type in self.active_buffs:
            pygame.draw.rect(screen, ITEM_TYPES[buff_type]['color'], (
                int(self.pos_x - PLAYER_WIDTH/2),
                int(self.screen_y - PLAYER_HEIGHT/2),
                PLAYER_WIDTH,
                PLAYER_HEIGHT
            ), border_thickness)
            border_thickness += 2

        # 긍정 버프 테두리
        if self.positive_buff:
            pygame.draw.rect(screen, ITEM_TYPES[self.positive_buff]['color'], (
                int(self.pos_x - PLAYER_WIDTH/2),
                int(self.screen_y - PLAYER_HEIGHT/2),
                PLAYER_WIDTH,
                PLAYER_HEIGHT
            ), border_thickness)

        # 활성화된 버프 아이콘을 화면 우측 상단에 그리기
        icon_size = 20
        icon_spacing = 5
        start_x = SCREEN_WIDTH - icon_size - 10
        start_y = 10

        # 긍정 버프 아이콘
        if self.positive_buff:
            pygame.draw.rect(screen, ITEM_TYPES[self.positive_buff]['color'], (
                start_x,
                start_y,
                icon_size,
                icon_size
            ))
            start_y += icon_size + icon_spacing

        # 중첩 가능한 버프 아이콘들
        for buff_type in self.active_buffs:
            pygame.draw.rect(screen, ITEM_TYPES[buff_type]['color'], (
                start_x,
                start_y,
                icon_size,
                icon_size
            ))
            start_y += icon_size + icon_spacing

    def update_screen_position(self, camera_y):
        """화면상의 위치를 업데이트합니다."""
        self.screen_y = self.pos_y - camera_y

    def update_score(self):
        """점수(높이)를 업데이트합니다."""
        # 시작 위치로부터의 현재 높이를 계산 (위로 갈수록 y값이 작아짐)
        # SCREEN_HEIGHT - 100 이 시작 위치이므로, 이를 기준으로 계산
        self.raw_height = max(0, abs(
            int((SCREEN_HEIGHT - 100 - self.pos_y) / 100)))  # 100픽셀당 1m

        # 난이도 배율 적용
        current_height = int(
            self.raw_height * Platform.current_difficulty.score_multiplier)

        # 현재 높이를 score에 반영
        self.score = current_height

        # 최고 높이 업데이트 (배율 적용된 값으로)
        if current_height > self.max_height:
            self.max_height = current_height
