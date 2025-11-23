# PS 3: Intelligent Travel & Budget Planner - Implementation Summary

## Overview
This is a LangGraph-based agent that demonstrates intelligent travel planning with constrained optimization and scenario generation. The system validates budget constraints and generates alternative travel plans when needed.

---

## Key Requirements & Implementation

### ✅ 1. CONSTRAINT SATISFACTION

**Requirement:** Agent logic to validate constraints (e.g., budget ≤ $1000) and adjust the plan.

**Implementation:**
- **`validate_budget_constraint()`** function: Validates if total cost is within budget limit
- **`check_budget_constraint()` node**: Implements the constraint validation logic
  - Calculates cost overage percentage
  - Determines if constraint is satisfied or violated
  - Flags violation to trigger scenario generation
  
**Key Features:**
- Clear constraint violation detection with percentage calculations
- Automatic routing to scenario generation when constraints are exceeded
- Conditional edge logic ensures proper flow based on validation result

**Example Output:**
```
--- 💰 CONSTRAINT VALIDATION ---
    Cost: $4305.18
    Budget Limit: $1000.00
    ❌ Constraint VIOLATED: $3305.18 over budget (330.5% excess)
    → Generating lower-cost alternatives...
```

---

### ✅ 2. STRUCTURED ITINERARY OUTPUT

**Requirement:** Generate a day-wise itinerary in a reliable format (e.g., JSON or Markdown Table).

**Implementation:**
- **`generate_day_itinerary()`**: Creates structured day-by-day itinerary with:
  - Date and day number
  - Hourly activities with time and description
  - Cost per activity
  - Daily subtotal

- **`format_itinerary_as_table()`**: Converts itinerary to Markdown table format for readability
- **`format_itinerary_as_json()`**: Converts itinerary to JSON format for programmatic access

**Data Structure:**
```python
itinerary = [
    {
        "day": 1,
        "date": "2025-11-23",
        "activities": [
            {"time": "08:00", "activity": "Breakfast at hotel", "cost": 25},
            {"time": "10:00", "activity": "Guided tour", "cost": 75},
            ...
        ],
        "daily_cost": 235.00
    },
    ...
]
```

**Example Output (Markdown Table):**
```
| Day | Date | Activities | Daily Cost |
|-----|------|-----------|------------|
| 1 | 2025-11-23 | Breakfast at hotel, Guided tour..., Dinner | $235.00 |
| 2 | 2025-11-24 | Breakfast at hotel, Guided tour..., Dinner | $235.00 |
...
```

**Cost Breakdown by Category:**
```
Cost Breakdown:
  • Flights: $463.75
  • Accommodation: $971.43
  • Meals: $875.00
  • Activities: $1645.00
  • Miscellaneous: $350.00
```

---

### ✅ 3. SCENARIO GENERATION

**Requirement:** Logic to create and present alternative, lower-cost versions of the plan.

**Implementation:**
- **`generate_scenario_output()` node**: Generates 3 distinct alternative scenarios when budget is exceeded

**Scenario Types:**

1. **Scenario 1: Shorter Duration**
   - Reduces trip length by 2-3 days
   - Focuses on top-priority activities
   - Maintains premium accommodations for shorter stay
   - Strategy: Cut trip short

2. **Scenario 2: Budget-Friendly Experience**
   - Maintains full duration
   - Reduces premium costs (downgrade accommodations, select free activities)
   - Use local transportation and restaurants
   - Skip premium guided tours
   - Strategy: Keep duration, reduce quality/comfort

3. **Scenario 3: Ultra-Budget Adventure**
   - Aggressive cost cutting
   - Hostels/budget hotels
   - Street food and local eateries
   - Free activities only
   - Public transportation exclusively
   - Strategy: Maximize budget stretch

**Each Scenario Includes:**
- Description and duration/adjustments
- Estimated cost
- Savings vs. original plan (in dollars)
- Specific, actionable adjustments

**Example Output:**
```
Scenario 1: Shorter Duration
  Description: Reduce trip from 7 to 5 days
  💵 Estimated Cost: $3075.13
  💰 Savings vs Original: $1230.05
  Key Adjustments:
    - Eliminate slower travel days
    - Focus on top-priority activities
    - Stay in premium accommodations for fewer nights

Scenario 2: Budget-Friendly Experience
  Description: Maintain full duration but reduce premium activities
  💵 Estimated Cost: $3228.88
  💰 Savings vs Original: $1076.29
  Key Adjustments:
    - Choose economy accommodations instead of 4-star hotels
    - Select free or low-cost activities (parks, markets, beaches)
    - Eat at local restaurants instead of tourist zones
    - Skip premium guided tours; use self-guided options

Scenario 3: Ultra-Budget Adventure
  Description: Minimal costs with local travel focus
  💵 Estimated Cost: $950.00
  💰 Savings vs Original: $3355.18
  Key Adjustments:
    - Book flights 2+ months in advance or use budget airlines
    - Stay in hostels or budget hotels
    - Cook some meals; eat street food and local eateries
    - Participate only in free activities
    - Use public transportation exclusively

✅ RECOMMENDED: Scenario 3: Ultra-Budget Adventure
   Cost: $950.00 (within budget: $1000.00)
```

---

## Graph Architecture

### State Definition
```python
class TravelPlannerState(TypedDict):
    user_request: str                    # Original user request
    destination: str                     # Travel destination
    duration_days: int                   # Trip duration in days
    itinerary: List[Dict]                # Day-wise activities and costs
    cost_breakdown: Dict[str, float]    # Costs by category (flights, accommodation, etc.)
    plan_notes: str                      # Formatted output
    total_cost: float                    # Total estimated cost
    budget_limit: float                  # Maximum allowed budget
    budget_ok: Literal["yes", "no"]     # Constraint satisfaction flag
    alternative_scenarios: List[Dict]    # Alternative cost scenarios
```

### Nodes & Edges

```
START
  ↓
[plan_trip] - Generates initial itinerary and calculates costs
  ↓
[check_constraints] - Validates budget constraint
  ↓
  ├─ (budget OK) → END
  └─ (budget exceeded) → [adjust_plan] → END
```

### Node Functions

1. **`generate_initial_plan()`**
   - Generates day-wise itinerary
   - Calculates cost breakdown
   - Returns structured output with both JSON and Markdown formats

2. **`check_budget_constraint()`**
   - Validates: total_cost ≤ budget_limit
   - Sets budget_ok flag ("yes" or "no")
   - Calculates overage percentage for reporting

3. **`generate_scenario_output()`**
   - Creates 3 alternative scenarios (if constraint violated)
   - Each scenario includes cost savings and adjustments
   - Recommends best scenario within budget
   - Returns detailed comparison

### Conditional Routing

```python
def route_on_budget(state: TravelPlannerState) -> Literal["ok", "fail"]:
    if state["budget_ok"] == "yes":
        return "ok"      # → END
    else:
        return "fail"    # → adjust_plan node
```

---

## Usage Example

```python
# Define travel request with budget constraint
user_request_data = {
    "user_request": "Plan a 7-day cruise to the Mediterranean, including flights.",
    "destination": "Mediterranean",
    "duration_days": 7,
    "budget_limit": 1000.00,  # Budget constraint
    "plan_notes": "",
    "total_cost": 0.0,
    "itinerary": [],
    "cost_breakdown": {},
    "budget_ok": "no",
    "alternative_scenarios": []
}

# Invoke the graph
final_result = graph.invoke(user_request_data)

# Access results
print(final_result['plan_notes'])                # Formatted output
print(final_result['total_cost'])                # Total cost
print(final_result['alternative_scenarios'])     # Alternative options
```

---

## Testing

The implementation includes **two test cases**:

### Test Case 1: Budget Constraint Violation (330% over budget)
- Request: 7-day Mediterranean cruise
- Initial cost: $4,305.18
- Budget limit: $1,000.00
- Result: Generates 3 alternative scenarios, recommends ultra-budget option at $950.00

### Test Case 2: Budget Constraint Nearly Violated (5% over budget)
- Request: 3-day Barcelona getaway
- Initial cost: $2,107.86
- Budget limit: $2,000.00
- Result: Generates 3 alternative scenarios, recommends ultra-budget option at $1,900.00

Both test cases demonstrate the system's ability to:
1. ✅ Validate constraints accurately
2. ✅ Generate structured itineraries
3. ✅ Create meaningful alternative scenarios

---

## Key Technical Features

- **LangGraph Integration**: Uses StateGraph for workflow orchestration
- **Conditional Routing**: Route_on_budget function enables dynamic flow control
- **Type Safety**: TypedDict for state management with type hints
- **Structured Output**: Multiple format support (JSON, Markdown tables)
- **Cost Breakdown**: Detailed cost analysis by category
- **Actionable Recommendations**: Each scenario includes specific adjustments

---

## Dependencies

- `langgraph`: Graph-based workflow orchestration
- `google.generativeai`: LLM integration (currently configured but not used in demo)
- `typing`: Type hints and declarations
- `json`: Structured data serialization
- `datetime`: Date handling for itinerary

---

## Future Enhancements

1. Integrate actual Gemini API calls for LLM-based itinerary generation
2. Add user preferences (food preferences, activity types, accessibility needs)
3. Real-time pricing integration (flights, hotels, activities)
4. Multi-destination routing optimization
5. Save and compare plans across multiple budgets
6. Integration with booking APIs (flights, accommodations)

---

## Conclusion

This implementation fully satisfies the PS 3 requirements by providing:
- ✅ **Constraint Satisfaction**: Robust budget validation with detailed violation reporting
- ✅ **Structured Itinerary Output**: Day-wise plans in both JSON and Markdown formats
- ✅ **Scenario Generation**: Multiple cost-reduction strategies with actionable recommendations
