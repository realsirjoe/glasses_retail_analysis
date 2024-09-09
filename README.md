# Glasses Retailer Data Analysis

[Interactive Version on Tableau](https://public.tableau.com/app/profile/sergio.wagenleitner/viz/GlassesProductAnalysis/Dashboard1)

[Source Code](https://github.com/realsirjoe/glasses_retail_analysis)

## Summary

Product analysis can be used to identify pricing correlations, competitive positioning, and enhance customer insights. This project collected data on 35K items from some of the largest opticians in Austria. The optician industry has a relatively small set of total items, which makes it easier to perform tests, validations, and experiments with the data. Additionally, the software can track prices and assist in developing a competitive pricing strategy.

Data was collected from four different retailers:
- Fielmann
- Mr Spex
- Pearle
- Hartlauer

Spanning a total of 259 brands.

The project can be split into three parts:
- Collection
- Transformation
- Visualization

## Collection

Since the data is not publicly available in a structured format, we had to scrape it from various retailer websites. Python was chosen in combination with Scrapy to enable easy and fast extraction. Often, the underlying API was utilized, and in cases where this wasn’t possible, the data was extracted from the HTML via BeautifulSoup. The spiders were able to extract all data in less than an hour. No proxies were required since the number of items was fairly small.

The items were stored in an SQLite database and later loaded into pandas.

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/dataframe.png?raw=true)

## Transformation

To enable fast experimentation, Jupyter was used at this stage.

Data cleaning was fairly straightforward, including lowercasing and stripping certain special characters. Another step involved translating German color names to English.

## Visualization

I was finally able to derive deeper insights from the collected data. Pandas and NumPy were used within Jupyter for this step. To begin, I looked at product quantities by retailer and brand.

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/retailer_product_count.png?raw=true)

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/brand_count.png?raw=true)

I also grouped prices to get a sense of which brands were expensive and which were cheaper.

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/expensive_brands.png?raw=true)

After analyzing correlations between color and price, I found that golden, black, and silver-colored glasses tend to be more expensive, while purple, pink, and transparent ones are on the cheaper side. To avoid outliers, only colors that appeared over 100 times were considered.

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/expensive_colors.png?raw=true)

To compare price differences between retailers, a straightforward approach would be to use a boxplot to group prices by retailer. While interesting, this would only describe their market positioning rather than which retailer has the cheapest products. Some might simply stock more expensive brands rather than selling the same products for higher prices.

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/brand_price_boxplot.png?raw=true)

A more refined approach would be to group prices by brand and then calculate a mean from the prices within each brand. This could serve as a good approximation but could still suffer from the same issue mentioned above.

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/brand_price_relative_mean_deviation.png?raw=true)

To answer the question of which retailer offers the best prices, the ideal solution—though more complex—would be to match all products from all retailers and compare their differences, thus comparing identical items and eliminating the aforementioned problem. However, this turns out to be rather difficult.

### Unique IDs

An easy method to match products would be to use a unique identifier across retailers, but these don’t always exist, or may not exist at all for some retailers. A more resilient solution would be to match by all or a subset of product fields in an intelligent way.

### TF-IDF

I used Term Frequency-Inverse Document Frequency (TF-IDF) to solve this problem. First, the search term had to be broken down into tokens, which could simply be words separated by spaces or fixed-size chunks of the term. The term frequency counts these tokens for every search term. The Inverse Document Frequency looks at how unique the terms are across all search terms. By multiplying the two, words that are frequent in a product but rare across all products will have a high TF-IDF score.

&nbsp;

By adding the color code to the product, this method worked fairly well. The best tokenization algorithm was to create one big string of data from the product and split it into chunks/ngrams of length 3. I also experimented with prioritizing the front and adding words separated by spaces as tokens, but these produced poorer results. In general, the simpler method worked well and matched a large portion of the products.

As a side effect, I created a way to match products and generate price intelligence for retailers to stay competitive.

Retailers didn’t always provide the exact same product with matching colors, so the number of matches was smaller than the number of unique products.

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/brand_price_real_relative_mean_deviation.png?raw=true)

If we compare this chart with the simple method of grouping items by brand and calculating the mean, we can see a strong correlation. Most of the time, values are very close to each other, and the previous chart turns out to be a good approximation.

Therefore, if we know which brand(s) we want to buy but aren’t sure which item, we could make a retailer choice based on this chart. It could also be used as a metric for retailers to evaluate their pricing strategy.

Of course, we can now also answer the question of which retailer offers the best price for a specific item.

# Possible Enhancements

- Increase the number of items as well as industries and make it a more general tool.

- Product matching could be improved by incorporating a transformer-based approach, training with labeled data, and matching via product images.

- Collect popularity metrics for all items as well as retailer size metrics to estimate relative or even total profits.

