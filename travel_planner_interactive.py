"""
Interactive Travel Planner - User-friendly CLI interface
Allows you to create custom travel plans with your own preferences
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, List, Dict
import google.generativeai as ai
import random
import json
from datetime import datetime, timedelta
import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- CONFIGURATION ---
ai.configure(api_key="AIzaSyD4oyCJx2iedzFxJDqhN1dLhjRoavqFDFo")
model = ai.GenerativeModel('gemini-2.5-flash')

# --- STATE DEFINITION ---
class TravelPlannerState(TypedDict):
    user_request: str
    destination: str
    duration_days: int
    itinerary: List[Dict]
    cost_breakdown: Dict[str, float]
    plan_notes: str
    total_cost: float
    budget_limit: float
    budget_ok: Literal["yes", "no"]
    alternative_scenarios: List[Dict]

# --- HELPER FUNCTIONS ---

def generate_day_itinerary(day: int, destination: str) -> Dict:
    """Generate a single day's itinerary with activities and costs."""
    activities = [
        {"time": "08:00", "activity": "Breakfast at hotel", "cost": 25},
        {"time": "10:00", "activity": f"Guided tour of {destination} landmarks", "cost": 75},
        {"time": "13:00", "activity": "Lunch at local restaurant", "cost": 40},
        {"time": "15:00", "activity": "Museum or cultural site", "cost": 35},
        {"time": "18:00", "activity": "Dinner and evening entertainment", "cost": 60}
    ]
    return {
        "day": day,
        "date": (datetime.now() + timedelta(days=day-1)).strftime("%Y-%m-%d"),
        "activities": activities,
        "daily_cost": sum(a["cost"] for a in activities)
    }

def format_itinerary_as_table(itinerary: List[Dict]) -> str:
    """Format itinerary as a Markdown table."""
    table = "| Day | Date | Activities | Daily Cost |\n"
    table += "|-----|------|-----------|------------|\n"
    for day_plan in itinerary:
        activities_list = ", ".join([a["activity"] for a in day_plan["activities"]])
        table += f"| {day_plan['day']} | {day_plan['date']} | {activities_list} | ${day_plan['daily_cost']:.2f} |\n"
    return table

def calculate_cost_breakdown(duration_days: int) -> Dict[str, float]:
    """Calculate cost breakdown by category."""
    daily_activity_cost = duration_days * 235
    flights_cost = random.uniform(300, 600)
    accommodation_cost = duration_days * random.uniform(80, 150)
    meals_cost = duration_days * 125
    miscellaneous = duration_days * 50
    
    return {
        "flights": flights_cost,
        "accommodation": accommodation_cost,
        "meals": meals_cost,
        "activities": daily_activity_cost,
        "miscellaneous": miscellaneous
    }

def validate_budget_constraint(total_cost: float, budget_limit: float) -> bool:
    """Validate if cost is within budget constraint."""
    return total_cost <= budget_limit

# --- GRAPH NODE FUNCTIONS ---

def generate_initial_plan(state: TravelPlannerState) -> TravelPlannerState:
    """Node 1: Generates initial plan with structured itinerary and cost estimates."""
    print("\n[PLANE] Generating Initial Plan and Cost Estimates...\n")
    
    duration_days = state.get("duration_days", 7)
    destination = state.get("destination", "Mediterranean")
    
    itinerary = [generate_day_itinerary(day, destination) for day in range(1, duration_days + 1)]
    cost_breakdown = calculate_cost_breakdown(duration_days)
    total_cost = sum(cost_breakdown.values())
    
    plan_notes = f"[PLAN] TRAVEL PLAN: {state['user_request']}\n\n"
    plan_notes += "=== Day-wise Itinerary ===\n"
    plan_notes += format_itinerary_as_table(itinerary) + "\n\n"
    plan_notes += "=== Cost Breakdown ===\n"
    for category, cost in cost_breakdown.items():
        plan_notes += f"  * {category.capitalize()}: ${cost:.2f}\n"
    plan_notes += f"\n[OK] Initial Total Cost: ${total_cost:.2f}\n"
    
    print(f"   >> Generated {duration_days}-day itinerary for {destination}")
    print(f"   >> Estimated Total Cost: ${total_cost:.2f}")
    
    return {
        "itinerary": itinerary,
        "cost_breakdown": cost_breakdown,
        "plan_notes": plan_notes,
        "total_cost": total_cost,
        "alternative_scenarios": []
    }

def check_budget_constraint(state: TravelPlannerState) -> TravelPlannerState:
    """Node 2: Validates budget constraint."""
    print(f"\n[MONEY] Checking Budget Constraint...")
    print(f"    Cost: ${state['total_cost']:.2f}")
    print(f"    Budget Limit: ${state['budget_limit']:.2f}")
    
    constraint_satisfied = validate_budget_constraint(state['total_cost'], state['budget_limit'])
    
    if constraint_satisfied:
        print("    [OK] Budget constraint SATISFIED!")
        return {"budget_ok": "yes"}
    else:
        overage = state['total_cost'] - state['budget_limit']
        percent_over = (overage / state['budget_limit']) * 100
        print(f"    [WARNING] Budget EXCEEDED by ${overage:.2f} ({percent_over:.1f}%)")
        print(f"    >> Generating lower-cost alternatives...")
        return {"budget_ok": "no"}

def generate_scenario_output(state: TravelPlannerState) -> TravelPlannerState:
    """Node 3: Generates alternative cost scenarios."""
    print("\n[LIGHTBULB] Creating Alternative Scenarios...\n")
    
    original_cost = state['total_cost']
    budget = state['budget_limit']
    itinerary = state['itinerary']
    duration = len(itinerary)
    
    scenarios = []
    
    # Scenario 1: Shorter Duration
    reduced_duration = max(3, duration - 2)
    scenario1_cost = original_cost * (reduced_duration / duration)
    scenario1 = {
        "scenario": "Scenario 1: Shorter Duration",
        "description": f"Reduce trip from {duration} to {reduced_duration} days",
        "cost": scenario1_cost,
        "savings": original_cost - scenario1_cost,
        "adjustments": [
            "- Eliminate slower travel days",
            "- Focus on top-priority activities",
            "- Stay in premium accommodations for fewer nights"
        ]
    }
    scenarios.append(scenario1)
    
    # Scenario 2: Budget-friendly
    scenario2_cost = original_cost * 0.75
    scenario2 = {
        "scenario": "Scenario 2: Budget-Friendly Experience",
        "description": "Maintain full duration but reduce premium activities",
        "cost": scenario2_cost,
        "savings": original_cost - scenario2_cost,
        "adjustments": [
            "- Choose economy accommodations instead of 4-star hotels",
            "- Select free or low-cost activities (parks, markets, beaches)",
            "- Eat at local restaurants instead of tourist zones",
            "- Skip premium guided tours; use self-guided options"
        ]
    }
    scenarios.append(scenario2)
    
    # Scenario 3: Ultra-Budget
    scenario3_cost = budget * 0.95
    scenario3 = {
        "scenario": "Scenario 3: Ultra-Budget Adventure",
        "description": "Minimal costs with local travel focus",
        "cost": scenario3_cost,
        "savings": original_cost - scenario3_cost,
        "adjustments": [
            "- Book flights 2+ months in advance or use budget airlines",
            "- Stay in hostels or budget hotels",
            "- Cook some meals; eat street food and local eateries",
            "- Participate only in free activities",
            "- Use public transportation exclusively"
        ]
    }
    scenarios.append(scenario3)
    
    final_response = state['plan_notes'] + "\n" + "="*70 + "\n"
    final_response += "[WARNING] BUDGET CONSTRAINT VIOLATION\n"
    final_response += f"   Original Cost: ${original_cost:.2f} | Budget Limit: ${budget:.2f}\n"
    final_response += f"   Overage: ${original_cost - budget:.2f}\n\n"
    
    final_response += "[TARGET] ALTERNATIVE SCENARIOS:\n"
    final_response += "="*70 + "\n\n"
    
    for i, scenario in enumerate(scenarios, 1):
        final_response += f"{scenario['scenario']}\n"
        final_response += f"  Description: {scenario['description']}\n"
        final_response += f"  [PRICE] Estimated Cost: ${scenario['cost']:.2f}\n"
        final_response += f"  [SAVE] Savings vs Original: ${scenario['savings']:.2f}\n"
        final_response += f"  Key Adjustments:\n"
        for adj in scenario['adjustments']:
            final_response += f"    {adj}\n"
        final_response += "\n"
    
    best_scenario = min(scenarios, key=lambda x: abs(x['cost'] - budget)) if scenarios else scenarios[0]
    final_response += f"[OK] RECOMMENDED: {best_scenario['scenario']}\n"
    final_response += f"   Cost: ${best_scenario['cost']:.2f} (within budget: ${budget:.2f})\n"
    final_response += "="*70 + "\n"
    
    print(f"   >> Generated {len(scenarios)} alternative scenarios")
    print(f"   >> Best option: ${best_scenario['cost']:.2f}")
    
    return {
        "plan_notes": final_response,
        "alternative_scenarios": scenarios
    }

def route_on_budget(state: TravelPlannerState) -> Literal["ok", "fail"]:
    """Routes based on budget validation."""
    if state["budget_ok"] == "yes":
        return "ok"
    else:
        return "fail"

# --- BUILD GRAPH ---
builder = StateGraph(TravelPlannerState)
builder.add_node("plan_trip", generate_initial_plan)
builder.add_node("check_constraints", check_budget_constraint)
builder.add_node("adjust_plan", generate_scenario_output)

builder.add_edge(START, "plan_trip")
builder.add_edge("plan_trip", "check_constraints")
builder.add_conditional_edges(
    "check_constraints",
    route_on_budget,
    {
        "ok": END,
        "fail": "adjust_plan"
    }
)
builder.add_edge("adjust_plan", END)

graph = builder.compile()

# --- INTERACTIVE CLI ---

def get_user_input():
    """Collect travel preferences from user."""
    print("\n" + "="*70)
    print("[APP] INTERACTIVE TRAVEL PLANNER")
    print("="*70 + "\n")
    
    print("Let's plan your next adventure!\n")
    
    # Get destination
    destination = input("Where do you want to go? (e.g., Paris, Tokyo, Hawaii): ").strip()
    if not destination:
        destination = "Mediterranean"
    
    # Get duration
    while True:
        try:
            duration = int(input("How many days? (e.g., 3-14): ").strip())
            if 1 <= duration <= 30:
                break
            print("Please enter a number between 1 and 30")
        except ValueError:
            print("Please enter a valid number")
    
    # Get budget
    while True:
        try:
            budget = float(input("What's your budget? (e.g., 1000): $").strip())
            if budget > 0:
                break
            print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")
    
    return destination, duration, budget

def save_plan(result, filename):
    """Save plan to JSON file."""
    output = {
        "plan": result['plan_notes'],
        "total_cost": result['total_cost'],
        "scenarios": result['alternative_scenarios'],
        "generated_at": datetime.now().isoformat()
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n[OK] Plan saved to: {filename}")

def main():
    """Main interactive loop."""
    while True:
        destination, duration, budget = get_user_input()
        
        print("\n" + "="*70)
        print(f"[PLAN] Trip: {duration} days in {destination}")
        print(f"[BUDGET] Maximum: ${budget:.2f}")
        print("="*70)
        
        user_request = f"Plan a {duration}-day trip to {destination}."
        
        request_data = {
            "user_request": user_request,
            "destination": destination,
            "duration_days": duration,
            "plan_notes": "",
            "total_cost": 0.0,
            "itinerary": [],
            "cost_breakdown": {},
            "budget_limit": budget,
            "budget_ok": "no",
            "alternative_scenarios": []
        }
        
        result = graph.invoke(request_data)
        
        print("\n" + "="*70)
        print("[RESULT] Your Travel Plan:")
        print("="*70)
        print(result['plan_notes'])
        
        # Ask to save
        save_choice = input("\nSave plan to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = f"travel_plan_{destination}_{duration}days.json"
            save_plan(result, filename)
        
        # Ask to plan another
        another = input("\nPlan another trip? (y/n): ").strip().lower()
        if another != 'y':
            print("\n[OK] Thanks for using Travel Planner! Have a great trip!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[EXIT] Travel Planner closed.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
