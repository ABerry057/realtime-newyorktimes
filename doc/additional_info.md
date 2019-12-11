[!New_York_Times_logo](\assets\nyt_icon.jpg)

This project leverages the official NYT api (https://developer.nytimes.com/apis). The data set used is built incrementally with every 
call to the API. As a result, the size of the data set is only limited by the maximum allowed calls to the API with our API key 
(10 API calls per minute). The data is then stored using MongoDB and transformed through NLP techniques. The output of the NLP  
function returns a nested list where each element (list) in the larger list contained the ID number of the article and another nested 
list within the list containing the article keywords. To transform the data, the nest list was passed through a function that returns 
a list for each article in the following format : [{keyword: count}]. A list comprehension is used to sort the most frequently occurring 
words and is then converted into a pandas dataframe. The pandas dataframe is then visualized via plotly and the resulting webapp 
is constructed in Dash and interactive graph is made possible through plotly. The resulting tech stack is the NYT api to MongoDB to Dash. This stack is illustrated below:

[!tech_stack](\assets\schem.jpg)

