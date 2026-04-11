- **Habit Tracker**: "Build a daily habit tracking spreadsheet with monthly overview"
- **Inventory Tracker**: "Create an inventory management spreadsheet with stock levels, reorder points, and valuation"
- **Sales Tracker**: "Build a sales pipeline tracker with stages, probabilities, and forecasting"
- **Time Tracker**: "Create a timesheet template with projects, hours, and billing calculations"

### Business Tools

Operational spreadsheets:

- **Invoice Template**: "Create a professional invoice template with automatic calculations"
- **Employee Directory**: "Build an employee directory spreadsheet with contact info, departments, and start dates"
- **Vendor Comparison**: "Create a vendor comparison spreadsheet for evaluating suppliers"
- **OKR Tracker**: "Build an OKR tracking spreadsheet for quarterly goals"
- **Meeting Agenda**: "Create a meeting agenda template with action items tracking"

### Analysis Templates

Data analysis and calculations:

- **Break-Even Analysis**: "Create a break-even analysis spreadsheet with charts"
- **Scenario Analysis**: "Build a scenario planning spreadsheet with what-if analysis"
- **Pricing Calculator**: "Create a pricing model spreadsheet with cost-plus and value-based options"
- **Loan Calculator**: "Build a loan amortization schedule with payment breakdown"
- **Commission Calculator**: "Create a sales commission calculator with tiered rates"

---

## Spreadsheet Features

CellCog spreadsheets can include:

| Feature | Description |
|---------|-------------|
| **Formulas** | SUM, AVERAGE, IF, VLOOKUP, and complex calculations |
| **Formatting** | Headers, colors, borders, number formats, conditional formatting |
| **Charts** | Bar, line, pie charts embedded in sheets |
| **Multiple Sheets** | Organized workbooks with linked sheets |
| **Data Validation** | Dropdowns, input restrictions |
| **Named Ranges** | For cleaner formulas |
| **Print Layout** | Ready for printing/PDF |

---

## Output Formats

| Format | Best For |
|--------|----------|
| **XLSX** | Editable in Excel, Google Sheets, Numbers |
| **Interactive HTML** | Web-based calculators and tools |

---

## Chat Mode for Spreadsheets

| Scenario | Recommended Mode |
|----------|------------------|
| Budget templates, trackers, data tables, basic calculations | `"agent"` |
| Complex financial models with multi-scenario analysis, intricate formulas | `"agent team"` |

**Default to `"agent"`** for most spreadsheet requests. CellCog's agent mode handles formulas, formatting, charts, and data organization efficiently.

Reserve `"agent team"` for complex financial modeling requiring deep accuracy validation—like DCF models, multi-scenario projections, or interconnected workbooks where formula correctness is critical.

---

## Example Spreadsheet Prompts

**SaaS financial model:**
> "Create a 3-year SaaS financial model with:
> 
> **Assumptions Sheet:**
> - Starting MRR: $10,000
> - Monthly growth rate: 15%
> - Churn rate: 3%
> - Average revenue per customer: $99
> - CAC: $500
> - Gross margin: 80%
> 
> **Monthly P&L:** Revenue, COGS, Gross Profit, Operating Expenses (broken down), Net Income
> 
> **Key Metrics:** MRR, ARR, Customers, Churn, LTV, CAC, LTV:CAC ratio
> 
> **Charts:** MRR growth, customer growth, profitability timeline
> 
> Include scenario toggles for growth rate (10%, 15%, 20%)."

**Personal budget:**
> "Create a monthly personal budget spreadsheet:
> 
> **Income Section:** Salary, side income, other
> 
> **Fixed Expenses:** Rent, utilities, insurance, subscriptions, loan payments
> 
> **Variable Expenses:** Groceries, dining out, transportation, entertainment, shopping, health
> 
> **Savings:** Emergency fund, retirement, vacation fund
> 
> Include:
> - Monthly summary with % of income per category
> - Year-at-a-glance sheet with monthly totals
> - Pie chart showing expense breakdown
> - Conditional formatting (red if over budget)
> 
> Assume $5,000/month income."

**Sales tracker:**
> "Build a sales pipeline tracker spreadsheet with:
> 
> **Columns:** Company, Contact, Deal Value, Stage (dropdown: Lead, Qualified, Proposal, Negotiation, Closed Won, Closed Lost), Probability, Expected Close Date, Notes, Last Contact
> 
> **Calculations:** Weighted pipeline value, deals by stage, win rate
> 
> **Dashboard Sheet:** Pipeline by stage (funnel chart), monthly forecast, top 10 deals, activity metrics
> 
> Include sample data for 20 deals."

**Break-even analysis:**
> "Create a break-even analysis spreadsheet:
> 
> **Inputs:**
> - Fixed costs (rent, salaries, etc.)
> - Variable cost per unit
> - Selling price per unit
> 
> **Calculations:**
> - Break-even units
> - Break-even revenue
> - Margin of safety
> 
> **Sensitivity table:** Show break-even at different price points
> 
> **Chart:** Cost-volume-profit graph showing break-even point
> 
> Default values: Fixed costs $50,000/month, variable cost $15/unit, price $25/unit."

---

## Tips for Better Spreadsheets

1. **Specify the structure**: List the sheets, columns, and calculations you need.

2. **Provide assumptions**: For financial models, give starting numbers and growth rates.

3. **Mention formulas needed**: "Include VLOOKUP for...", "Calculate running totals", "Show variance vs plan."

4. **Request sample data**: "Include realistic sample data for testing" helps see it in action.

5. **Describe formatting**: "Conditional formatting for negative values", "Currency format", "Freeze header row."

6. **Chart preferences**: "Include a line chart showing trend", "Pie chart for breakdown."
