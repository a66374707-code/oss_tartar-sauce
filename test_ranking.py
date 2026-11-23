import contextlib
import io
import os
import tempfile
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


class TestGetTopN(unittest.TestCase):
    """get_top_n(): 점수 높은 순으로 정렬해 상위 n개만 돌려주는지 검사한다."""

    def test_점수_높은_순으로_정렬된다(self):
        records = {"amy": 100, "bob": 300, "cat": 200}
        self.assertEqual(ranking.get_top_n(records),
                         [("bob", 300), ("cat", 200), ("amy", 100)])

    def test_n개만_돌려준다(self):
        records = {"amy": 100, "bob": 300, "cat": 200}
        self.assertEqual(ranking.get_top_n(records, 2),
                         [("bob", 300), ("cat", 200)])

    def test_기본값은_상위_10개(self):
        records = {f"user{i}": i for i in range(12)}
        top = ranking.get_top_n(records)
        self.assertEqual(len(top), 10)
        self.assertEqual(top[0], ("user11", 11))


class TestRecordFile(unittest.TestCase):
    """load_records / save_records: 파일 저장·불러오기와 손상된 파일 처리를 검사한다."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "r.json")

    def test_파일이_없으면_빈_기록(self):
        self.assertEqual(ranking.load_records(self.path), {})

    def test_저장한_기록을_그대로_불러온다(self):
        ranking.save_records({"amy": 500, "bob": 300}, self.path)
        self.assertEqual(ranking.load_records(self.path), {"amy": 500, "bob": 300})

    def test_손상된_파일은_빈_기록(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{ 깨진 내용")
        with contextlib.redirect_stdout(io.StringIO()):   # 오류 메시지 출력을 숨김
            self.assertEqual(ranking.load_records(self.path), {})

    def test_형식이_틀린_파일은_빈_기록(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("[1, 2, 3]")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ranking.load_records(self.path), {})


if __name__ == "__main__":
    unittest.main()