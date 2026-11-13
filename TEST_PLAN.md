# Test plan

Run automated tests from the project root:

```bash
python -m unittest discover -s tests -v
```

## Functional test cases

| ID | Test | Expected result |
|---|---|---|
| T01 | Open `/` | Dashboard returns HTTP 200 and shows KPI cards. |
| T02 | Open products page | Seed product catalogue is visible. |
| T03 | Add product with unique SKU | Product is saved and appears in catalogue. |
| T04 | Add duplicate SKU | Save is rejected with an error message. |
| T05 | Add negative price or stock | Input is rejected. |
| T06 | Decrease stock below zero | Stock is unchanged and error is shown. |
| T07 | Create bill for available stock | Bill and line item are saved; stock is deducted. |
| T08 | Create bill for more than available stock | Bill is rejected; stock is unchanged. |
| T09 | Search products | Results match product name, SKU or category. |
| T10 | Open a bill detail page | Receipt shows saved items and total. |
| T11 | Search sales | Matching customer/bill records are displayed. |

## Automated coverage
`tests/test_app.py` exercises dashboard rendering, product creation/duplicate SKU handling, negative stock prevention, successful billing, and insufficient-stock rollback using a temporary database.

## Manual testing evidence checklist
Before submission, run the app in your browser and capture your own screenshots of:
1. Dashboard with KPIs and stock alerts.
2. Product catalogue and search.
3. Add/edit product form.
4. Stock adjustment.
5. Bill creation with calculated total.
6. Final receipt.
7. Sales history.

Record any bugs found and the fix made. Do not claim a manual test passed unless you actually performed it.
