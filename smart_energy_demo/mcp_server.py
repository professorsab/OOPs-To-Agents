from flask import Flask, request, jsonify
from pydantic import BaseModel

app = Flask(__name__)

class Tariff(BaseModel):
    peak_rate: float=25.5
    off_peak_rate: float=15.2
    peak_hours_start: int=18
    peak_hours_end: int=22
    currency: str="PKR"

@app.route("/mcp", methods=["POST"])
def mcp():
    j = request.json
    if j["method"]=="get_tariff":
        t = Tariff()
        result = t.dict()
        result["location"]="karachi"; result["provider"]="K‑Electric"
        return jsonify({"jsonrpc":"2.0","result": result, "id": j["id"]})
    return jsonify({"jsonrpc":"2.0","error": {"code":-32601,"message":"Method not found"}, "id": j["id"]})

if __name__=="__main__":
    app.run(port=5001)
