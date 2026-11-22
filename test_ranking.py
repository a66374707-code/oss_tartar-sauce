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


if __name__ == "__main__":
    unittest.main()