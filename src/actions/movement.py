from ..constants import *


class Movement:
    @staticmethod
    def apply_gravity(player, platforms):
        """
        중력을 적용하고 플랫폼과의 충돌을 처리합니다.
        Args:
            player: 플레이어 객체
            platforms: 플랫폼 객체 리스트
        """
        prev_y = player.pos_y

        # 중력 적용
        player.velocity_y += GRAVITY
        player.pos_y += player.velocity_y

        # 플랫폼과의 충돌 검사
        player_bottom = player.bottom
        prev_bottom = prev_y + PLAYER_HEIGHT/2

        # 현재 플레이어가 서있는 플랫폼
        current_platform = None

        for platform in platforms:
            # 사라진 상태의 플랫폼은 무시
            if hasattr(platform, 'is_vanish') and platform.is_vanish and not platform.is_visible:
                continue

            # 플레이어가 떨어지는 중일 때만 충돌 체크
            if player.velocity_y > 0:
                # 플레이어의 바닥과 플랫폼 상단의 충돌 검사
                if (prev_bottom <= platform.y and  # 이전 프레임에서는 플랫폼보다 위에 있었고
                        player_bottom >= platform.y):  # 현재 프레임에서는 플랫폼보다 아래로 이동했으며

                    # 플레이어의 중심이 플랫폼 범위 안에 있는지 확인
                    if (platform.x <= player.pos_x <= platform.x + platform.width):
                        # 플랫폼 위에 착지
                        player.pos_y = platform.y - PLAYER_HEIGHT/2
                        player.velocity_y = 0
                        player.is_jumping = False
                        current_platform = platform
                        break

            # 이미 플랫폼 위에 서 있는 경우 (점프하지 않은 상태)
            elif not player.is_jumping:
                # 플레이어의 중심이 플랫폼 범위 안에 있는지 확인
                if (platform.y - 5 <= player_bottom <= platform.y + 5 and
                        platform.x <= player.pos_x <= platform.x + platform.width):
                    current_platform = platform
                    break

        # 움직이는 플랫폼 위에 있을 경우 플랫폼과 함께 이동
        if current_platform and current_platform.is_moving and not player.is_jumping:
            player.pos_x += current_platform.speed * current_platform.direction

        # 현재 서있는 플랫폼이 사라진 상태라면 플레이어를 떨어지게 함
        if current_platform and hasattr(current_platform, 'is_vanish') and current_platform.is_vanish and not current_platform.is_visible:
            player.is_jumping = True
            current_platform = None

    @staticmethod
    def move_horizontal(player, direction):
        """플레이어를 좌우로 이동시킵니다."""
        player.pos_x += direction * PLAYER_SPEED
        # 화면 경계 처리
        player.pos_x = max(
            PLAYER_WIDTH/2, min(SCREEN_WIDTH - PLAYER_WIDTH/2, player.pos_x))

    @staticmethod
    def jump(player):
        """플레이어 점프를 실행합니다."""
        if not player.is_jumping:
            player.velocity_y = JUMP_POWER
            player.is_jumping = True
            return True
        return False


class Land:
    @staticmethod
    def execute(player, platform_y):
        """플레이어를 발판 위에 착지시킵니다."""
        print(f"발판 위에 착지: {platform_y}")
        player.absolute_y = platform_y - PLAYER_HEIGHT/2
        player.velocity_y = 0
        player.is_jumping = False
        return True
