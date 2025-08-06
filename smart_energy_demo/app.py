from flask import Flask, render_template, request
import requests
import uuid, datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MCP_SERVER = "http://localhost:5001/mcp"
AGENT_B = "http://localhost:5002/acp/optimize"

@app.route("/", methods=["GET", "POST"])
def home():
    steps = []
    recommendation = None
    current_step = 1
    appliance = ""
    time = ""
    
    if request.method == "POST":
        preferred_time = request.form.get("time", "")
        appliance = request.form.get("appliance", "")
        current_step = int(request.form.get("step", 1))
        
        # Set the time variable for template rendering
        time = preferred_time
        
        print(f"DEBUG: Form data - appliance: '{appliance}', time: '{preferred_time}', step: {current_step}")
        
        # Only use default fallback if time is completely empty
        if not preferred_time or preferred_time.strip() == "":
            preferred_time = "08:00"  # Changed default to 8 AM for testing
            time = preferred_time
            print(f"DEBUG: Using default time: {preferred_time}")
            
        try:
            # Step 1: MCP Server Call
            if current_step >= 1:
                req = {"jsonrpc":"2.0","method":"get_tariff","params":{"type":"residential","location":"karachi"},"id":1}
                mcp_response = requests.post(MCP_SERVER, json=req, timeout=10)
                
                if mcp_response.status_code == 200:
                    m = mcp_response.json()
                    tariff = m["result"]
                    
                    steps.append({
                        "title": "🔍 Electricity Tariff Retrieved Successfully (MCP Protocol)",
                        "status": "✅ MCP Response Received",
                        "status_class": "status-success",
                        "description": "Successfully retrieved current electricity tariff data from K-Electric via MCP protocol.",
                        "data": tariff,
                        "type": "tariff"
                    })
                else:
                    steps.append({
                        "title": "🔍 MCP Server Error",
                        "status": f"❌ MCP Error ({mcp_response.status_code})",
                        "status_class": "status-error",
                        "description": f"MCP Server returned error status: {mcp_response.status_code}. Please ensure MCP Server is running on port 5001.",
                        "type": "info"
                    })
                    return render_template("home.html", steps=steps, current_step=current_step, appliance=appliance, time=time)

            # Step 2: ACP Message Preparation
            if current_step >= 2:
                acp = {
                    "type":"request", 
                    "agent_id":"agentA",
                    "timestamp": datetime.datetime.utcnow().isoformat()+"Z",
                    "correlation_id": str(uuid.uuid4()),
                    "task":"optimize_appliance_schedule",
                    "data": {
                        "appliance_type": appliance, 
                        "preferred_time": preferred_time,  # Make sure this is passed correctly
                        "tariff_context": tariff
                    }
                }
                
                print(f"DEBUG: ACP message preferred_time: '{preferred_time}'")
                
                steps.append({
                    "title": "📤 ACP Message Prepared (Agent Communication Protocol)",
                    "status": "✅ Ready to Send",
                    "status_class": "status-success",
                    "description": "JSON-structured ACP message created with appliance details and tariff context.",
                    "data": json.dumps(acp, indent=2),
                    "type": "json"
                })

            # Step 3: AI Agent Processing
            if current_step >= 3:
                print(f"DEBUG: Sending to Agent B - Time: '{preferred_time}'")
                agent_response = requests.post(AGENT_B, json=acp, timeout=30)
                
                if agent_response.status_code == 200:
                    resp = agent_response.json()
                    
                    steps.append({
                        "title": "🤖 AI Analysis Complete (Smart Energy Logic)",
                        "status": "✅ Recommendation Generated",
                        "status_class": "status-success",
                        "description": "AI Agent analyzed your request and generated personalized recommendations based on peak/off-peak hour analysis.",
                        "type": "info"
                    })
                    
                    if resp.get("success"):
                        result = resp.get("result", {})
                        ai_reply = result.get("reply", "No recommendation available")
                        cost_analysis = result.get("cost_analysis", {})
                        recommendation_type = result.get("recommendation_type", "unknown")
                        
                        # Format recommendation with detailed cost analysis
                        cost_savings_text = ""
                        if cost_analysis.get("is_peak_time"):
                            # Peak time - show savings opportunity
                            cost_savings_text = f"""
🚨 PEAK HOUR DETECTED ({cost_analysis.get('user_hour', 'Unknown')}:00)
Current cost: {cost_analysis.get('current_cost', 0)} PKR
Off-peak cost: {cost_analysis.get('off_peak_cost', 0)} PKR
Potential savings: {cost_analysis.get('savings', 0)} PKR
Recommended time: {cost_analysis.get('optimal_time', '23:00')}
"""
                        else:
                            # Off-peak time - show approval
                            cost_savings_text = f"""
✅ OFF-PEAK HOURS - OPTIMAL TIMING! ({cost_analysis.get('user_hour', 'Unknown')}:00)
Current cost: {cost_analysis.get('current_cost', 0)} PKR
You're already getting the best rate!
Savings vs peak: {round((cost_analysis.get('power_consumption', 2.0) * 25.5) - cost_analysis.get('current_cost', 0), 2)} PKR
"""
                        
                        recommendation = {
                            "message": ai_reply,
                            "cost_savings": cost_savings_text,
                            "recommendation_type": recommendation_type
                        }
                    else:
                        recommendation = {
                            "message": f"Error from AI Agent: {resp.get('error', 'Unknown error')}",
                            "cost_savings": None,
                            "recommendation_type": "error"
                        }
                        steps[-1]["status_class"] = "status-error"
                        steps[-1]["status"] = "❌ Error in AI Processing"
                        
                else:
                    steps.append({
                        "title": "🤖 AI Agent Error",
                        "status": f"❌ Agent B Error ({agent_response.status_code})",
                        "status_class": "status-error",
                        "description": f"AI Agent returned error status: {agent_response.status_code}. Please ensure Agent B is running on port 5002.",
                        "type": "info"
                    })
                    
        except requests.exceptions.ConnectionError as e:
            steps.append({
                "title": "🚨 Connection Error",
                "status": "❌ Service Unavailable",
                "status_class": "status-error",
                "description": "Cannot connect to required services. Please ensure both MCP Server (port 5001) and Agent B (port 5002) are running.",
                "type": "info"
            })
            
        except requests.exceptions.Timeout as e:
            steps.append({
                "title": "⏱️ Timeout Error",
                "status": "❌ Request Timeout",
                "status_class": "status-error",
                "description": "Request timed out. The AI agent might be processing a heavy load. Please try again.",
                "type": "info"
            })
            
        except Exception as e:
            steps.append({
                "title": "🚨 Unexpected Error",
                "status": "❌ System Error",
                "status_class": "status-error",
                "description": f"An unexpected error occurred: {str(e)}",
                "type": "info"
            })

    return render_template("home.html", steps=steps, recommendation=recommendation, current_step=current_step, appliance=appliance, time=time)

if __name__ == "__main__":
    app.run(debug=True)
