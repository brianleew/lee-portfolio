# Visualizations API
___
![Graph](https://media.tenor.com/F-LgB1xTebEAAAAd/look-at-this-graph-nickelback.gif)
## API Calls
___
### Bokeh
`bokeh.py` holds the `/api/vis/` route, which calls a util function to generate the bokeh plot for a given user, and
return the plot as a JSON dump to be rendered on the front end.
### Data
`data.py` holds the `/api/vis/data` route, which will fetch the real and prediction data for a given meter from the
database, format the data into JSON format, and return it to the front end.
