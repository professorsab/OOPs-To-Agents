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
    
    if request.method == "POST":
        preferred_time = request.form["time"]
        appliance = request.form["appliance"]
        
        # Step 1: User Input
        steps.append({
            "title": "📝 Processing User Request",
            "status": "✅ Completed",
            "status_class": "status-success",
            "description": f"User wants to optimize {appliance} usage at {preferred_time}",
            "type": "info"
        })
        
        try:
            # Step 2: MCP Server Call
            steps.append({
                "title": "🔍 Fetching Electricity Tariff Data (MCP Protocol)",
                "status": "🔄 Connecting to MCP Server...",
                "status_class": "status-processing",
                "description": "Sending JSON-RPC request to Model Context Protocol server to retrieve current electricity tariff information for Karachi.",
                "type": "info"
            })
            
            req = {"jsonrpc":"2.0","method":"get_tariff","params":{"type":"residential","location":"karachi"},"id":1}
            
            mcp_response = requests.post(MCP_SERVER, json=req, timeout=10)
            
            if mcp_response.status_code == 200:
                m = mcp_response.json()
                tariff = m["result"]
                
                steps[-1] = {
                    "title": "🔍 Electricity Tariff Retrieved Successfully",
                    "status": "✅ MCP Response Received",
                    "status_class": "status-success",
                    "description": "Successfully retrieved current electricity tariff data from K-Electric via MCP protocol.",
                    "data": tariff,
                    "type": "tariff"
                }
                
                # Step 3: Preparing ACP Message
                steps.append({
                    "title": "📤 Preparing Agent Communication (ACP Protocol)",
                    "status": "⚙️ Building JSON Message",
                    "status_class": "status-processing",
                    "description": "Creating structured JSON message using Agent Communication Protocol (ACP) to send to AI optimization agent.",
                    "type": "info"
                })
                
                acp = {
                    "type":"request", 
                    "agent_id":"agentA",
                    "timestamp": datetime.datetime.utcnow().isoformat()+"Z",
                    "correlation_id": str(uuid.uuid4()),
                    "task":"optimize_appliance_schedule",
                    "data": {
                        "appliance_type": appliance, 
                        "preferred_time": preferred_time, 
                        "tariff_context": tariff
                    }
                }
                
                steps[-1] = {
                    "title": "📤 ACP Message Prepared",
                    "status": "✅ Ready to Send",
                    "status_class": "status-success",
                    "description": "JSON-structured ACP message created with appliance details and tariff context.",
                    "data": json.dumps(acp, indent=2),
                    "type": "json"
                }
                
                # Step 4: Agent B Communication
                steps.append({
                    "title": "🤖 AI Agent Processing (Agent B)",
                    "status": "🧠 Analyzing with OpenAI GPT...",
                    "status_class": "status-processing",
                    "description": "Sending request to AI Agent B which uses OpenAI GPT-3.5-turbo to analyze optimal appliance scheduling based on electricity tariffs.",
                    "type": "info"
                })
                
                agent_response = requests.post(AGENT_B, json=acp, timeout=30)
                
                if agent_response.status_code == 200:
                    resp = agent_response.json()
                    
                    steps[-1] = {
                        "title": "🤖 AI Analysis Complete",
                        "status": "✅ Recommendation Generated",
                        "status_class": "status-success",
                        "description": "AI Agent successfully analyzed your request and generated personalized recommendations using advanced energy optimization algorithms.",
                        "type": "info"
                    }
                    
                    # Step 5: Final Results
                    steps.append({
                        "title": "📊 Results & Recommendations",
                        "status": "✅ Analysis Complete",
                        "status_class": "status-success",
                        "description": "Complete analysis finished with cost optimization suggestions and alternative scheduling recommendations.",
                        "type": "info"
                    })
                    
                    if resp.get("success"):
                        result = resp.get("result", {})
                        ai_reply = result.get("reply", "No recommendation available")
                        cost_analysis = result.get("cost_analysis", {})
                        
                        # Format recommendation with cost savings
                        cost_savings_text = ""
                        if cost_analysis.get("savings", 0) > 0:
                            cost_savings_text = f"""
                            Current cost at {preferred_time}: {cost_analysis.get('current_cost', 0)} PKR
                            Cost during off-peak hours: {cost_analysis.get('off_peak_cost', 0)} PKR
                            You can save {cost_analysis.get('savings', 0)} PKR by switching to {cost_analysis.get('optimal_time', '22:30')}!
                            """
                        elif cost_analysis.get("savings", 0) == 0:
                            cost_savings_text = f"Great choice! You're already using off-peak hours. Current cost: {cost_analysis.get('current_cost', 0)} PKR"
                        
                        recommendation = {
                            "message": ai_reply,
                            "cost_savings": cost_savings_text
                        }
                    else:
                        recommendation = {
                            "message": f"Error from AI Agent: {resp.get('error', 'Unknown error')}",
                            "cost_savings": None
                        }
                        steps[-1]["status_class"] = "status-error"
                        steps[-1]["status"] = "❌ Error in AI Processing"
                        
                else:
                    steps[-1] = {
                        "title": "🤖 AI Agent Error",
                        "status": f"❌ Agent B Error ({agent_response.status_code})",
                        "status_class": "status-error",
                        "description": f"AI Agent returned error status: {agent_response.status_code}. Please ensure Agent B is running on port 5002.",
                        "type": "info"
                    }
                    
            else:
                steps[-1] = {
                    "title": "🔍 MCP Server Error",
                    "status": f"❌ MCP Error ({mcp_response.status_code})",
                    "status_class": "status-error",
                    "description": f"MCP Server returned error status: {mcp_response.status_code}. Please ensure MCP Server is running on port 5001.",
                    "type": "info"
                }
                
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

    return render_template("home.html", steps=steps, recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
