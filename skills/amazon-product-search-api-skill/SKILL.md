---
name: amazon-product-search-api-skill
description: "This skill is designed to help users automatically extract product data from Amazon search results. The Agent should proactively apply this skill when users request searching for products related to keywords, finding best-selling items from specific brands, monitoring product prices and availability on Amazon, extracting product listings for market research, collecting product ratings and review counts for competitive analysis, finding specific products with a maximum count, searching Amazon in different languages for localized results, tracking monthly sales estimates for brand products, gathering product URLs and titles for a product catalog, scanning Amazon for Best Seller tags in a specific category, monitoring shipping and delivery information for brand items, building a structured dataset of Amazon search results."
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["python"],"env":["BROWSERACT_API_KEY"]}}}
---

# Amazon Product Search Automation Skill

## 📖 Introduction
This skill provides a one-stop product data collection service through BrowserAct's Amazon Product Search API template. It directly extracts structured product results from Amazon search lists. Simply input search keywords, brand filters, and quantity limits to get clean, usable product data.

## ✨ Features
1. **No Hallucinations**: Pre-set workflows avoid AI generative hallucinations, ensuring stable and precise data extraction.
2. **No Captcha Issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP Restrictions**: No need to handle regional IP restrictions or geofencing.
4. **Faster Execution**: Tasks execute faster compared to pure AI-driven browser automation solutions.
5. **Cost-Effective**: Significantly lowers data acquisition costs compared to high-token-consuming AI solutions.

## 🔑 API Key Setup
Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not take other measures; ask and wait for the user to provide it.
**Agent must inform the user**:
> "Since you haven't configured the BrowserAct API Key, please visit the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key."

## 🛠️ Input Parameters
When calling the script, the Agent should flexibly configure the following parameters based on user needs:

1. **KeyWords (Search Keywords)**
   - **Type**: `string`
   - **Description**: The keywords the user wants to search for on Amazon.
   - **Example**: `phone`, `wireless earbuds`, `laptop stand`

2. **Brand (Brand Filter)**
   - **Type**: `string`
   - **Description**: Filter products by brand name shown in the listing.
   - **Example**: `Apple`, `Samsung`, `Sony`

3. **Maximum_date (Maximum Products)**
   - **Type**: `number`
   - **Description**: The maximum number of products to extract across paginated search results.
   - **Default**: `50`

4. **language (UI Language)**
   - **Type**: `string`
   - **Description**: UI language for the Amazon browsing session.
   - **Options**: `en`, `de`, `fr`, `it`, `es`, `ja`, `zh-CN`, `zh-TW`
   - **Default**: `en`

## 🚀 Usage
The Agent should execute the following independent script to achieve "one-line command result":

```bash
# Example Call
python -u ./scripts/amazon_product_search_api.py "Keywords" "Brand" Quantity "language"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script result, keep monitoring the terminal output.
- As long as the terminal is outputting new status logs, the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- Only if the status remains unchanged for a long time or the script stops outputting without returning a result should you consider triggering the retry mechanism.

## 📊 Data Output
After successful execution, the script will parse and print results directly from the API response. Results include:
- `product_title`: Product name
- `product_url`: Detail page URL
- `rating_score`: Average star rating
- `review_count`: Total number of reviews
- `monthly_sales`: Estimated monthly sales (if available)
- `current_price`: Current selling price
- `list_price`: Original list price (if available)
- `delivery_info`: Delivery or fulfillment information
- `shipping_location`: Shipping origin or location
- `is_best_seller`: Whether marked as Best Seller
- `is_available`: Whether available for purchase

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations or task failure), the Agent should follow this logic:

1. **Check Output Content**:

## 详细文档

请参阅 [references/details.md](references/details.md)
