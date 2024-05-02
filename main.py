import pandas as pd
import plotly.express as px

## update settings for float values to only 2 decimal places
pd.options.display.float_format = '{:,.2f}'.format
## create dataframe for the apps in the csv
df_apps = pd.read_csv('apps.csv')
## read samples of the data
df_apps.shape
df_apps.head()
df_apps.sample(5)

## drop unneeded columns to minimize data
df_apps.drop(["Last_Updated", "Android_Ver"], axis=1, inplace=True)
df_apps.head()

## show the rows with NAN data
nan_rows = df_apps[df_apps.Rating.isna()]
print(nan_rows.shape)
print(nan_rows.head())

## get rid of data entries in the Rating column where there is a NAN
df_clean_app = df_apps.dropna()
df_clean_app.shape

## show duplicate rows 
duplicate_rows = df_clean_app[df_clean_app.duplicated()]
print(duplicate_rows.shape)
duplicate_rows.head()

## specifically show how many instagrams exist
df_clean_app[df_clean_app.App == "Instagram"]

## update the clean df to drop duplicate rows if the app name, app type, and app price all match
df_clean_app = df_clean_app.drop_duplicates(subset=["App","Type", "Price"])

## show that we only have one instagram now
df_clean_app[df_clean_app.App == "Instagram"]

## and that we have trimmed off quite a few rows
## 9367 down to 8199
df_clean_app.shape

## identify the highest rated application
highest_rating_id = df_clean_app['Rating'].idxmax()
print(df_clean_app.loc[highest_rating_id])
## sort the data based on the rating and show the top 5 rated applications
df_clean_app.sort_values('Rating', ascending=False).head()

## show the largest in size -- clearly a size limit of 100.0 mbs is in place
df_clean_app.sort_values('Size_MBs', ascending=False).head()

## show the 50 applications with the most reviews -- all of which are free
df_clean_app.sort_values('Reviews', ascending=False).head(50)

## make a table of only the content rating and the quantity of each
ratings = df_clean_app.Content_Rating.value_counts()
print(ratings)

## build a pie chart out of the table we just made of content ratings and quantity 
## this creates a pie graph object
ratings_pie = px.pie(labels=ratings.index, values=ratings.values)
ratings_pie

## update the parameters of the graph object to show more data from the ratings table we made
ratings_pie = px.pie(labels=ratings.index, values=ratings.values, title="Content Rating", names=ratings.index)
ratings_pie.update_traces(textposition="outside", textinfo="percent+label")
ratings_pie.show()

## change it to a doughnut shape
ratings_pie = px.pie(labels=ratings.index, values=ratings.values, title="Content Rating", names=ratings.index, hole=0.6,)
ratings_pie.update_traces(textposition="inside", textfont_size=15, textinfo="percent")
ratings_pie.show()


## determine how many installs of different apps 
df_clean_app.Installs.describe()
df_clean_app.info()

## present the data to determine what needs to be cleaned off
df_clean_app[["App", "Installs",]].groupby("Installs").count()

## clean off the nan values and the commas
df_clean_app.Installs = df_clean_app.Installs.astype(str).str.replace(',', '')
df_clean_app.Installs = pd.to_numeric(df_clean_app.Installs)
df_clean_app[["App", "Installs",]].groupby("Installs").count()

## comvert price column to numeric values also
df_clean_app.Price.describe()
df_clean_app.Price = df_clean_app.Price.astype(str).str.replace('$', '')
df_clean_app.Price = pd.to_numeric(df_clean_app.Price)
df_clean_app.sort_values("Price", ascending=False).head()

## clean off fake applications 
df_clean_app = df_clean_app[df_clean_app["Price"] < 250]
df_clean_app.sort_values("Price", ascending=False).head(5)

## build a revenue estimate column
df_clean_app["Revenue Estimate"] = df_clean_app.Installs.mul(df_clean_app.Price)
df_clean_app.sort_values("Revenue Estimate", ascending=False)[:10]

## identify the top 10 categories of apps
top10_category = df_clean_app.Category.value_counts()[:10]
print(top10_category)

## build a bar graph of the quatity of apps in each category
bar = px.bar(x = top10_category.index, y = top10_category.values)
bar.show()

## group the apps by category, and then add up how many installs happen in each category
category_installs = df_clean_app.groupby("Category").agg({"Installs": pd.Series.sum})
category_installs.sort_values("Installs", ascending=True, inplace=True)

## build a bar graph out of the new data showing how many installs per category occur
h_bar = px.bar(x = category_installs.Installs, y = category_installs.index, orientation = 'h', title="Category Popularity")
h_bar.update_layout(xaxis_title="Number of Downloads", yaxis_label="Category")
h_bar.show()

## update the look of the graph
h_bar = px.bar(x = category_installs.Installs, y = category_installs.index, orientation='h', title='Category Popularity')
h_bar.update_layout(xaxis_title='Number of Downloads', yaxis_title='Category')
h_bar.show()

## make a df of the apps quanity per category
category_number = df_clean_app.groupby("Category").agg({"App": pd.Series.count})

## merge the two category df's into a single df to show downloads per category and how many apps per category
category_merged_df = pd.merge(category_number, category_installs, on="Category", how="inner")

## show the shape 
print(f"The dimentions of the new Category Merged df are: {category_merged_df.shape}")
## display the actual df we just made
category_merged_df.sort_values("Installs", ascending=False)

## create a scatter plot of the new df
scatter_category = px.scatter(category_merged_df, x="App", y="Installs", title="Category Concentration", size="App", hover_name=category_merged_df.index, color="Installs")
scatter_category.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)", yaxis_title="Installs", yaxis=dict(type="log"))
scatter_category.show()

## examine the genres column 
len(df_clean_app.Genres.unique())
## show that some are separated by ; instead of new entries 
df_clean_app.Genres.value_counts().sort_values(ascending=True)[:5]

## separate each genre accurately
stack = df_clean_app.Genres.str.split(';', expand=True).stack()
print(f"The new column only shows the descrete genres: {stack.shape}")

## count up the genres and display them
num_genres = stack.value_counts()
print(f"The number of unique genres: {len(num_genres)}")

## make a bar graph of the genres and how many apps per genre exist
genre_bar = px.bar(x = num_genres.index[:15], y = num_genres.values[:15], hover_name=num_genres.index[:15], color=num_genres.values[:15], color_continuous_scale="Agsunset")
genre_bar.update_layout(xaxis_title="Genre", yaxis_title="Number of Apps", coloraxis_showscale=False)
genre_bar.show()

## show how many different types of apps are in each genre
df_clean_app.Type.value_counts()
## make a df of how many paid and how many free apps per genre are in the list
df_free_vs_paid = df_clean_app.groupby(["Category", "Type"], as_index=False).agg({"App": pd.Series.count})
df_free_vs_paid.head()

## make a bargraph from the df we just made showing the differences in quanitity of free vs paid apps per category
bar_free_vs_paid = px.bar(df_free_vs_paid, x="Category", y="App", title="Free vs Paid Apps By Category", color="Type", barmode="group")
bar_free_vs_paid.update_layout(xaxis_title="Category", yaxis_title="Number of Apps", xaxis={"categoryorder": "total descending"}, yaxis=dict(type='log'))
bar_free_vs_paid.show()

## make a box graph comparing how many downloads paid vs free apps in the same genre have
installs_box = px.box(df_clean_app, y='Installs', x="Type", color="Type", notched=True, points="all", title="How Many Downloads do Paid Apps Give Up?")
installs_box.update_layout(yaxis=dict(type="log"))
installs_box.show()

## make a box graph showing how much a paid app can expect to earn
df_paid_apps = df_clean_app[df_clean_app['Type'] == 'Paid']
paid_box = px.box(df_paid_apps, x='Category', y='Revenue Estimate', title='How Much Can Paid Apps Earn?')  
paid_box.update_layout(xaxis_title='Category', yaxis_title='Paid App Ballpark Revenue', xaxis={'categoryorder':'min ascending'}, yaxis=dict(type='log'))  
paid_box.show()

## showing the median price for apps in each category
df_paid_apps.Price.median()
med_price_box = px.box(df_paid_apps, x='Category', y='Price', title='Price Per Category')  
med_price_box.update_layout(xaxis_title='Category', yaxis_title='Paid App Price', xaxis={'categoryorder':'max descending'}, yaxis=dict(type='log'))  
med_price_box.show()
