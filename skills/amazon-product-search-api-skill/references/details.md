   - If the output **contains** `"Invalid authorization"`, it means the API Key is invalid or expired. **Do not retry**; guide the user to re-check and provide the correct API Key.
   - If the output **does not contain** `"Invalid authorization"` but the task failed (e.g., output starts with `Error:` or returns empty results), the Agent should **automatically try to re-execute the script once**.

2. **Retry Limit**:
   - Automatic retry is limited to **one time**. If the second attempt fails, stop retrying and report the specific error information to the user.

## 🌟 Typical Use Cases
1. **Market Research**: Search for "wireless earbuds" from "Sony" to analyze the current market.
2. **Competitive Monitoring**: Track "Samsung" phone prices and availability on Amazon.
3. **Catalog Discovery**: Gather product titles and URLs for a new product catalog in the "laptop stand" category.
4. **Localized Analysis**: Search Amazon in "ja" (Japanese) to understand products available in the Japan region.
5. **Best Seller Tracking**: Identify products marked as "Best Seller" for a specific brand.
6. **Pricing Intelligence**: Compare `current_price` and `list_price` to monitor discounts.
7. **Sales Trend Estimation**: Use `monthly_sales` data to estimate market demand for certain items.
8. **Shipping Efficiency Study**: Analyze `delivery_info` and `shipping_location` for various brands.
9. **Large-scale Data Extraction**: Collect up to 100 products for a comprehensive dataset.
10. **Product Availability Check**: Verify if specific brand products are currently `is_available` for purchase.
