## Did countries have good responses to the COVID-19 pandemic? 
The question that we will aim to solve is to cluster countries into categories based on their responses to the COVID-19 pandemic. To do so we used two clustering models. For our models, we had to create metrics that we can measure the success of the countries response on.

### Quality Metrics

#### Stringency Index

For the stringency index, one of our datasets had an engineered index to measure the strictness of the countries. Each day, the country was given a value based on its policies and current responses to the COVID-19 pandemic. For the purposes of our clustering algorithm, we took these values and averaged each days value between January 1, 2020 and November 1, 2020. This gave each country a single stringency value that we used for our clustering.

#### Case Growth

Similar to the stringency index, we had a dataset that included the per capita number of new cases each day for each country. We averaged this growth over the duration of the pandemic to give each country a single growth value that we could use for our clustering.

#### Time until Closure

The final metric that we used in our clustering algoirthm was the time until closure metric. This measured the number of days from January 1, 2020 that a country began to impose restrictions on in person events, specifically students attending school in person.

We also investigated a couple of other metrics, but they ended up giving us worse results than just these 3. To avoid overfitting, we dropped those, but you can see more of this investigation in the jupyter notebook.

### Clustering Algorithms

We decided to perform two different clustering algorithms on this problem to investigate the quality of responses. We performed Agglomerative Clustering and K-Means clustering.  You can see our results in the jupyter notebook.
