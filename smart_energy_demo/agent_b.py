from flask import Flask, request, jsonify
import openai
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Updated OpenAI client initialization
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def calculate_cost_savings(appliance_type, preferred_time, tariff):
    """Calculate potential cost savings and suggest optimal time"""
    
    # Estimated power consumption (kWh) for different appliances
    appliance_power = {
        "dryer": 3.0,
        "washing machine": 0.5,
        "dishwasher": 1.8,
        "water heater": 4.0,
        "air conditioner": 3.5,
        "electric oven": 2.4,
        "pool pump": 1.1
    }
    
    power_consumption = appliance_power.get(appliance_type.lower(), 2.0)
    
    # Parse preferred time
    try:
        hour = int(preferred_time.split(':')[0])
    except:
        hour = 19
    
    peak_start = tariff['peak_hours_start']
    peak_end = tariff['peak_hours_end']
    peak_rate = tariff['peak_rate']
    off_peak_rate = tariff['off_peak_rate']
    
    # Check if preferred time is in peak hours
    is_peak_time = peak_start <= hour <= peak_end
    
    current_cost = power_consumption * (peak_rate if is_peak_time else off_peak_rate)
    off_peak_cost = power_consumption * off_peak_rate
    savings = current_cost - off_peak_cost if is_peak_time else 0
    
    # Suggest optimal time (just after peak hours end)
    optimal_hour = (peak_end + 1) % 24
    optimal_time = f"{optimal_hour:02d}:30"
    
    return {
        "is_peak_time": is_peak_time,
        "current_cost": round(current_cost, 2),
        "off_peak_cost": round(off_peak_cost, 2),
        "savings": round(savings, 2),
        "optimal_time": optimal_time,
        "power_consumption": power_consumption
    }

@app.route("/acp/optimize", methods=["POST"])
def optimize():
    try:
        msg = request.json
        data = msg["data"]
        ap = data["appliance_type"]
        pt = data["preferred_time"]
        tariff = data["tariff_context"]
        
        # Calculate cost analysis
        cost_analysis = calculate_cost_savings(ap, pt, tariff)
        
        # Enhanced prompt with cost analysis
        prompt = f"""
        Analyze the energy usage for {ap} at {pt} with the following information:
        
        Electricity Tariff:
        - Peak rate: {tariff['peak_rate']} PKR/kWh (Hours: {tariff['peak_hours_start']}:00-{tariff['peak_hours_end']}:00)
        - Off-peak rate: {tariff['off_peak_rate']} PKR/kWh
        
        Cost Analysis:
        - Estimated power consumption: {cost_analysis['power_consumption']} kWh
        - Cost at preferred time: {cost_analysis['current_cost']} PKR
        - Cost during off-peak: {cost_analysis['off_peak_cost']} PKR
        - Potential savings: {cost_analysis['savings']} PKR
        - Recommended optimal time: {cost_analysis['optimal_time']}
        
        Provide a detailed recommendation including:
        1. Whether the preferred time is cost-effective
        2. Specific cost savings if switched to off-peak hours
        3. Suggest the best time to run the appliance
        4. Include environmental benefits of off-peak usage
        
        Keep the response conversational and helpful.
        """
        
        # Updated OpenAI API call syntax
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        reply = response.choices[0].message.content.strip()
        
        result = {
            "reply": reply,
            "cost_analysis": cost_analysis,
            "tariff_info": tariff
        }
        
        return jsonify({
            "type": "response",
            "agent_id": "agentB",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "correlation_id": msg["correlation_id"],
            "success": True,
            "result": result
        })
        
    except Exception as e:
        # Return error response instead of crashing
        return jsonify({
            "type": "response",
            "agent_id": "agentB", 
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "correlation_id": msg.get("correlation_id", "unknown"),
            "success": False,
            "error": f"Error processing request: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(port=5002, debug=True)
