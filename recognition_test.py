
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# 모델 클래스와 구역 번호 연결
ZONE_MAP = {
    "LU": 1,
    "MU": 2,
    "RU": 3,
    "LM": 4,
    "MM": 5,
    "RM": 6,
    "LD": 7,
    "MD": 8,
    "RD": 9
}

# 신뢰도 기준: 80%
CONFIDENCE_THRESHOLD = 0.80

# 인식 결과 저장
latest_result = {
    "zone": None,
    "confidence": 0.0
}


@app.route("/")
def home():
    return send_from_directory("recognition", "index.html")


@app.route("/model/my_pose/<path:filename>")
def model_files(filename):
    return send_from_directory("model/my_pose", filename)


@app.route("/result", methods=["POST"])
def receive_result():
    data = request.get_json()

    label = data.get("label")
    confidence = data.get("confidence", 0)

    if label not in ZONE_MAP:
        return jsonify({"error": "Unknown label"}), 400

    # 신뢰도가 80% 미만이면 무효 처리
    if confidence < CONFIDENCE_THRESHOLD:
        latest_result["zone"] = None
        latest_result["confidence"] = confidence
    else:
        latest_result["zone"] = ZONE_MAP[label]
        latest_result["confidence"] = confidence

    print("인식 결과:", latest_result)

    return jsonify(latest_result)


@app.route("/latest")
def get_latest():
    return jsonify(latest_result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)