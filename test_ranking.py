import unittest

import ranking


class TestValidateNickname(unittest.TestCase):
    """validate_nickname(): 올바르면 None, 틀리면 안내 메시지를 반환하는지 검사한다."""

    def test_정상_닉네임은_None(self):
        self.assertIsNone(ranking.validate_nickname("amy1"))

    def test_빈_값은_오류(self):
        self.assertEqual(ranking.validate_nickname(""), "닉네임이 비어 있습니다.")

    def test_16자는_오류(self):
        self.assertIsNotNone(ranking.validate_nickname("a" * 16))

    def test_한글은_오류(self):
        self.assertIsNotNone(ranking.validate_nickname("홍길동"))


class TestUpdateRecord(unittest.TestCase):
    """update_record(): 같은 닉네임은 최고 점수 하나만 유지하는지 검사한다."""

    def test_새_닉네임은_추가된다(self):
        records = {}
        self.assertTrue(ranking.update_record(records, "amy", 100))
        self.assertEqual(records, {"amy": 100})

    def test_더_높은_점수는_갱신된다(self):
        records = {"amy": 100}
        self.assertTrue(ranking.update_record(records, "amy", 500))
        self.assertEqual(records, {"amy": 500})

    def test_더_낮은_점수는_무시된다(self):
        records = {"amy": 100}
        self.assertFalse(ranking.update_record(records, "amy", 50))
        self.assertEqual(records, {"amy": 100})


if __name__ == "__main__":
    unittest.main()