import json
import os


class RankingSystem:
    def __init__(self):
        self.rankings = []
        self.max_rankings = 10
        self.rankings_file = "rankings.json"
        self.load_rankings()
        self.current_player = None

    def load_rankings(self):
        """랭킹 데이터를 파일에서 로드합니다."""
        try:
            if os.path.exists(self.rankings_file):
                with open(self.rankings_file, 'r') as f:
                    self.rankings = json.load(f)
        except:
            self.rankings = []

    def save_rankings(self):
        """랭킹 데이터를 파일에 저장합니다."""
        with open(self.rankings_file, 'w') as f:
            json.dump(self.rankings, f)

    def add_score(self, nickname, score):
        """새로운 점수를 추가하고 랭킹을 업데이트합니다."""
        # 새로운 점수 추가
        new_record = {"nickname": nickname, "score": score}
        self.rankings.append(new_record)

        # 점수 기준으로 정렬
        self.rankings.sort(key=lambda x: x["score"], reverse=True)

        # 상위 10개만 유지
        self.rankings = self.rankings[:self.max_rankings]

        # 파일에 저장
        self.save_rankings()

        # 현재 순위 반환 (1-based)
        return next((i + 1 for i, r in enumerate(self.rankings)
                    if r["nickname"] == nickname and r["score"] == score), None)

    def is_nickname_taken(self, nickname):
        """닉네임이 이미 사용 중인지 확인합니다."""
        return any(r["nickname"] == nickname for r in self.rankings)

    def get_rank_for_score(self, score):
        """주어진 점수의 예상 순위를 반환합니다."""
        return next((i + 1 for i, r in enumerate(self.rankings)
                    if r["score"] <= score), len(self.rankings) + 1)

    def format_rankings(self):
        """랭킹을 표시용 문자열 리스트로 변환합니다."""
        formatted = []
        for i, record in enumerate(self.rankings, 1):
            formatted.append(f"{i}. {record['nickname']}: {record['score']}m")
        return formatted
