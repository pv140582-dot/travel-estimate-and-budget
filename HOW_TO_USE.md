# How to Use the Travel Planner

## Quick Start (2 Options)

### Option 1: Run the Demo (Pre-configured Test Cases)
```bash
python travel_planner.py
```
This shows two example trips with pre-set destinations and budgets. Great for seeing how the system works!

---

### Option 2: Run Interactive Mode (Your Custom Trip)
```bash
python travel_planner_interactive.py
```

When you run this, you'll be asked:
```
Where do you want to go? (e.g., Paris, Tokyo, Hawaii): [TYPE YOUR DESTINATION]
How many days? (e.g., 3-14): [TYPE NUMBER]
What's your budget? (e.g., 1000): $[TYPE AMOUNT]
```

**Example Input:**
```
Where do you want to go? Paris
How many days? 7
What's your budget? $2500
```

---

## What You'll Get

The system will generate:

1. **Day-by-Day Itinerary**
   - Activities scheduled for each day
   - Daily costs breakdown
   - Organized in a clean table format

2. **Cost Analysis**
   - Flights
   - Accommodation
   - Meals
   - Activities
   - Miscellaneous expenses

3. **Budget Check**
   - If within budget: Shows your final plan ✓
   - If over budget: Generates 3 alternative scenarios

4. **Alternative Scenarios (if needed)**
   - **Scenario 1**: Shorter Duration (cut trip short)
   - **Scenario 2**: Budget-Friendly (keep duration, reduce costs)
   - **Scenario 3**: Ultra-Budget (aggressive cost cutting)

---

## Example Output

```
[PLAN] TRAVEL PLAN: Plan a 7-day trip to Paris.

=== Day-wise Itinerary ===
| Day | Date | Activities | Daily Cost |
|-----|------|-----------|------------|
| 1 | 2025-11-23 | Breakfast, Guided tour, Lunch, Museum, Dinner | $235.00 |
| 2 | 2025-11-24 | Breakfast, Guided tour, Lunch, Museum, Dinner | $235.00 |
...

=== Cost Breakdown ===
  * Flights: $450.00
  * Accommodation: $840.00
  * Meals: $875.00
  * Activities: $1645.00
  * Miscellaneous: $350.00

[OK] Initial Total Cost: $4160.00
```

---

## Save Your Plan

After generating a plan, you can save it to a JSON file:
```
Save plan to file? (y/n): y
```

This creates a file like: `travel_plan_Paris_7days.json`

The saved file contains:
- Full itinerary
- Cost breakdown
- Alternative scenarios (if generated)
- Timestamp

---

## Tips for Best Results

✓ **Be specific with destination names** - Better recommendations for your location
✓ **Set realistic budgets** - The system helps find alternatives if you're over
✓ **Try different durations** - 3 days, 7 days, 14 days give different plans
✓ **Save good plans** - JSON files let you compare options

---

## Troubleshooting

**Q: Unicode/Emoji errors?**
A: The interactive version handles encoding better. Use `travel_planner_interactive.py`

**Q: Budget always shows as exceeded?**
A: This is normal! The planner generates realistic costs. Use the scenarios to optimize.

**Q: Can I modify the itinerary?**
A: Currently the planner is read-only. You can save plans and compare scenarios.

---

## Files

- `travel_planner.py` → Demo with pre-set test cases
- `travel_planner_interactive.py` → Your custom trip planner
- `travel_plan_*.json` → Your saved plans

---

## Features

✓ Day-wise activity scheduling
✓ Detailed cost breakdown by category
✓ Budget constraint validation
✓ Automatic scenario generation for over-budget trips
✓ Save plans to JSON
✓ Interactive CLI interface
✓ Multi-trip planning in one session

---

## Next Steps

1. Run the demo: `python travel_planner.py`
2. Try interactive mode: `python travel_planner_interactive.py`
3. Enter your dream destination
4. Explore alternatives and save your favorite plan!

Enjoy planning your next adventure! ✈️
