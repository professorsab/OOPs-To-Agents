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
    
    # Better time parsing with debugging
    print(f"DEBUG: Received preferred_time: '{preferred_time}'")
    
    try:
        if not preferred_time or preferred_time.strip() == "":
            print("DEBUG: Empty time, defaulting to 19:00")
            hour = 19
            minute = 0
        else:
            time_parts = preferred_time.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            print(f"DEBUG: Parsed hour: {hour}, minute: {minute}")
    except Exception as e:
        print(f"DEBUG: Time parsing error: {e}, defaulting to 19:00")
        hour = 19
        minute = 0
    
    peak_start = tariff['peak_hours_start']  # 18 (6 PM)
    peak_end = tariff['peak_hours_end']      # 22 (10 PM)
    peak_rate = tariff['peak_rate']          # 25.5 PKR
    off_peak_rate = tariff['off_peak_rate']  # 15.2 PKR
    
    # Check if preferred time is in peak hours (18:00 to 22:59)
    is_peak_time = peak_start <= hour <= peak_end
    
    print(f"DEBUG: Hour {hour} is_peak_time: {is_peak_time} (peak: {peak_start}-{peak_end})")
    
    current_cost = power_consumption * (peak_rate if is_peak_time else off_peak_rate)
    off_peak_cost = power_consumption * off_peak_rate
    savings = current_cost - off_peak_cost if is_peak_time else 0
    
    # Suggest optimal time (just after peak hours end - 23:00)
    optimal_hour = 23
    optimal_time = f"{optimal_hour:02d}:00"
    
    return {
        "is_peak_time": is_peak_time,
        "current_cost": round(current_cost, 2),
        "off_peak_cost": round(off_peak_cost, 2),
        "savings": round(savings, 2),
        "optimal_time": optimal_time,
        "power_consumption": power_consumption,
        "user_hour": hour,
        "user_minute": minute
    }

@app.route("/acp/optimize", methods=["POST"])
def optimize():
    try:
        msg = request.json
        data = msg["data"]
        ap = data["appliance_type"]
        pt = data["preferred_time"]
        tariff = data["tariff_context"]
        
        print(f"DEBUG: Received appliance: {ap}, time: '{pt}'")
        
        # Calculate cost analysis
        cost_analysis = calculate_cost_savings(ap, pt, tariff)
        
        # Format time for display
        display_time = pt if pt and pt.strip() else "Unknown Time"
        user_hour = cost_analysis["user_hour"]
        
        # Create specific response based on peak/off-peak analysis
        if cost_analysis["is_peak_time"]:
            # User selected PEAK HOURS (6 PM - 10 PM) - Suggest different time
            reply = f"""⚠️ **Peak Hour Alert!** 

Your selected time ({display_time} - {user_hour}:00) falls within peak hours (6:00 PM - 10:00 PM) when electricity rates are highest.

**Cost Analysis:**
- Running {ap} at {display_time}: **{cost_analysis['current_cost']} PKR**
- Running {ap} during off-peak: **{cost_analysis['off_peak_cost']} PKR**
- **You can save {cost_analysis['savings']} PKR** by waiting!

**💡 Recommended Times:** 
- **11:00 PM (23:00)** or later tonight
- **Early morning before 6:00 PM** tomorrow

**💰 Savings:** {cost_analysis['savings']} PKR per use
**🌱 Environmental Benefit:** Off-peak hours use cleaner energy from renewable sources

**Suggestion:** Wait until 11:00 PM or use early morning hours for maximum savings!"""

        else:
            # User selected OFF-PEAK HOURS - Approve the time
            peak_cost = round(cost_analysis['power_consumption'] * tariff['peak_rate'], 2)
            savings_vs_peak = round(peak_cost - cost_analysis['current_cost'], 2)
            
            reply = f"""✅ **Excellent Choice!** 

Your selected time ({display_time} - {user_hour}:00) is during off-peak hours when electricity rates are lowest.

**Cost Analysis:**
- Running {ap} at {display_time}: **{cost_analysis['current_cost']} PKR**
- This is already the optimal rate!
- **You're saving {savings_vs_peak} PKR** compared to peak hours

**🎉 You can proceed with using your {ap} at {display_time}**
**💰 Smart Choice:** You're paying the lowest possible rate ({tariff['off_peak_rate']} PKR/kWh)
**🌱 Eco-Friendly:** Off-peak energy is more environmentally sustainable

**Go ahead and start your {ap} at {display_time} - you're optimizing both cost and environmental impact!**"""

        result = {
            "reply": reply,
            "cost_analysis": cost_analysis,
            "tariff_info": tariff,
            "recommendation_type": "peak_warning" if cost_analysis["is_peak_time"] else "approved"
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
        print(f"DEBUG: Error in optimize: {e}")
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
