# Price Intelligence Austrian Glasses

Product analysis can be used to identify pricing correlations, competitive positioning and to enhance customer insights.
This project collected 35K items from some of the biggest opticians in Austria. The Optician industry has a fairly small set of total items which makes it easy to perform tests and validations and play around with the data. Further the software can track prices and assist in creating a competitive pricing strategy.

Data was collected from 4 different retailers:
- Fielmann
- Mr Spex
- Pearle
- Hartlauer

Spanning a total of 259 brands

The project can be split into three parts:
- Collection
- Transformation
- Visualization

## Collection

Since the data is not publicly available in a structured format we need to scrape it from the various retailer websites. Python has been choosen in combination with Scrapy to enable easy as well as fast extraction. Often the underlying API has been utilized in cases where this wasn't possible the data was extracted from the html via beautifulsoup. The spiders were able to extract all data in less than an hour, no proxies were required since the number of items was fairly small. 

The items were stored in an sqlite database

## Transformation

To enable fast experimentation jupyter was used at this stage. 

Data cleaning was fairly straightforward, including lowercasing as well as striping certain special characters. Another step involved translating german colors to english.

## Visualization

I was finally able to get deeper insights from the collected data. Pandas and Numpy were used inside jupyter for this step. To get started I looked at product quantities by retailer and brand. 

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/retailer_product_count.png?raw=true)

![alt text](https://github.com/realsirjoe/glasses_retail_analysis/blob/main/github_images/brand_count.png?raw=true)

I also grouped prices to get a feel for expensive or cheap brands.

After looking for correlations between color and price I found that golden, black and silver colors are pricey while purple, pink and transparent colors are on the cheaper side. To avoid outliers only colors that appeared over 100 times were considered

[photos here]

To compare price differences between retailers an easy approach would be to boxplot the prices grouped by retailer. While interesting to explore this would only describe their positioning in the market not which one has the cheapest products. Some might simply have more expensive brands rather than selling the same products for more. 

[photos here]

Another more refined approach would be to group by brand and then build a mean from that brands prices. This could be a good approximation but could still fall victim to the same problem mentioned above. 

[photos here]

To answer the question which retailer gives you the best prices the best solution though more complicated would be to match all products from all retailers and compare their difference therefore comparing the same items and removing the forementioned problem. 

However this turns out to be rather difficult. An easy method to match would be to use a unique identifier for a product across retailers but these don't always exist or may not exist at all for some retailers. A more resilient solution would be to match by all or a subset of product fields in some intelligent way. 

I used Term Frequency-Inverse Document Frequency (tf idf) to solve this problem. First the search term has to be broken down into tokens, which could simply be words seperated by spaces but also fixed size chunks of the term. The term frequency counts these tokens for every search term. The Inverse Document Frequency looks at how unique the terms are over all search terms. By multiplying the two Words that are frequent in a product but rare across all products will have a high TF-IDF score

By also adding the color code to the product this method worked fairly well. The best tokenization algorithm was to simply create one big string of data from the product and split it into chunks/ngrams of length 3. I also experimented with prioritizing the front and adding words seperated by space as tokens which produced poorer results. In general the simple method worked fairly well and matched a large portion of products.

As a side effect I created a way to match products and create price intelligence for retailers to stay competitive. 

Retailers didn't always provide the exact same product with the matching color so the number of our matches is smaller than the number of unique products. 

[ photos ]

If we compare the chart with the simple method that grouped items by brand and built the mean we can see a strong correlation. Most of the time values are very close to each other and the previous chart turns out to be good approximation. 

Therefore if we know what brand(s) we want to buy but are not sure which item we could make a retailer choice based on this chart. Also it could be used as a metric for retailers to evaluate their pricing strategy. 

Of course now we can also answer the question which retailer has the best price for a specific item. 

# Future Enhancements

If I had more time with this project I would increase the number of items as well as industries and make it a more general tool. 

Further product matching could be improved by incorperating a transformer based approach and train with labeled data. 

I would also aim to collect popularity metrics for all items as well as retailer size metrics and estimate relative or even total profits



The project can be split into three parts:


- Visualization
To draw conclusions about the data and visualize them jupyter, pandas, numpy and a view smaller packages were utilized. 

More complex analysis involved matching products from different retailers and comparing prices. term frequency and inverse document frequency (tf idf) was used for this challange. It was experimented to weight the beginning higher than the end of a string as well as add space seperated words to the tokens, next to ngrams but these turned out to perform poorer than simply using the algorithm with 3 letter ngrams. Matching could be improved by incorporating other machine learning techniques using labeled data but tf idf turned out to be sufficient for this project. 

[ photos here 
