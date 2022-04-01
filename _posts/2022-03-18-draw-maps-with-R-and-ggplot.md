---
layout: post
title: Draw beautiful maps with R and ggplot2 library
date: 2022-03-18
last_modified_at: 2022-03-18
excerpt:
  In this article we are going to learn how to draw maps using the R
  programming language and ggplot2 library. While I am mostly using
  Python for everything else, I must admit R produces beautiful figures and
  I have been using it extensively for data visualization, especially for
  drawing maps.
cover: maps-ggplot2.png
image: /assets/img/eric.jpg
categories: ["DataViz"]
---

## Download the datasets

First, let's download two public datasets that we will use to draw our maps.
Both datasets are from the city of New York. The first one is a
[polygon file](https://data.beta.nyc/dataset/nyc-zip-code-tabulation-areas/resource/894e9162-871c-4552-a09c-c6915d8783fb?view_id=2c40fce3-0bb2-46d3-bb67-04a935151a96),
in the geojson format. This file will let us draw the NYC county shapes. It
also contains census statistics on every county, such as their population and
area. The second file is a list of [restaurants](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j) in NYC, and their inspection
results. This is a csv file, where every restaurant is located with latitude
longitude coordinates, so that we can display them on a map. It also has
restaurants attributes such as cuisine description and inspection score.

- Download the [polygon file](https://data.beta.nyc/dataset/nyc-zip-code-tabulation-areas/resource/894e9162-871c-4552-a09c-c6915d8783fb?view_id=2c40fce3-0bb2-46d3-bb67-04a935151a96).
- Download the [restaurants dataset](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j).

## Install the required librairies

I am going to assume you have [R](https://www.r-project.org/)
installed, and a development environment
software like [R Studio](https://www.rstudio.com/) for instance.

Here are the librairies we are going to need for this project:

- [geojsonio](https://cran.r-project.org/web/packages/geojsonio/index.html)
- [broom](https://cran.r-project.org/web/packages/broom/vignettes/broom.html)
- [sf](https://cran.r-project.org/web/packages/sf/index.html)
- [osmdata](https://cran.r-project.org/web/packages/osmdata/vignettes/osmdata.html)
- [ggplot2](https://cran.r-project.org/web/packages/ggplot2/index.html)
- [dplyr](https://cran.r-project.org/web/packages/dplyr/index.html)
- [ggnewscale](https://cran.r-project.org/web/packages/ggnewscale/index.html)

Once installed, load them in R:

``` R
library(geojsonio)
library(broom)
library(sf)
library(osmdata)
library(ggplot2)
library(dplyr)
library(ggnewscale)
```

## Load the datasets in R

The two datasets we downloaded earlier should be named
`zip_code_040114.geojson`
and `DOHMH_New_York_City_Restaurant_Inspection_Results.csv`. I stored them
into a folder named `data`, and the following code will read these two
files in R.

We first read the geojson file, then convert it to a spatial data frame
indexed with zip code, so that we can display the counties shapes on a map.
We then load the restaurants, and keep only the first 100 entries for
clarity.

``` R
# NYC Geometry
spdf_file <- geojson_read(  # Read the geojson file
  "data/zip_code_040114.geojson",
  what = "sp"
)
stats_df <- as.data.frame(spdf_file)  # Export the census statistics in another data frame variable
spdf_file <- tidy(  # Convert it to a spatial data frame, with zip code as index
  spdf_file,
  region="ZIPCODE"  # Use ZIPCODE variable as index, the index will be named "id"
)

# Restaurants data
restaurants <- read.csv(  # Read the csv file as a data frame
    "data/DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
)
restaurants <- restaurants %>% head(100)  # Keep only the first 100 restaurants
restaurants <- restaurants %>%  # Replace missing inspection grades with NA
  mutate(GRADE=replace(GRADE, GRADE == "", NA))
```

## Drawing maps

There are different kind of maps you can draw, like
[Choropleth](https://r-graph-gallery.com/choropleth-map.html),
[Connection](https://r-graph-gallery.com/connection-map.html)
or [Bubble](https://r-graph-gallery.com/bubble-map.html) maps. In the
following sections, we are going to give various maps examples
based on the NYC datasets we downloaded. The code is provided and
explained.

The code is mostly similar for every map, and arranged in the following
manner:

``` R
ggplot() +  # ggplot init
  # 1. adding layers from here
  geom_polygon(data=...,        # layer data
               aes(x=long,      # longitude on x axis
                   y=lat,       # latitude on y axis
                   group=group, # polygons from the same county share the same group
                   fill=...),   # fill polygons with some variable
               color="black",   # polygons borders are colored in black
               size=.2) +       # polygons borders are .2 width
  # 2. plot settings from here
  theme_void() +                # remove all axes
  coord_map() +                 # change coordinate system to map
  scale_fill_distiller(...) +   # customize the color palette for fill
  labs(title=...,               # add titles and legends
       subtitle=...,
       fill=...)
```

### Choropleth maps

A choropleth map uses intensity of color to show an aggregate
metric, such as population density or per-capita income.

In the following map, we display the counties as polygons, and fill
them according to their population.

![map_1](/assets/img/articles/maps-ggplot2/map_1.png)

The data used for this map is a join between the spatial data frame and
the census statistics data frame. We join on `id` and `ZIPCODE`, as the spatial
data frame is indexed by `ZIPCODE`.

``` R
ggplot() +
  geom_polygon(data=spdf_file %>%
                 inner_join(stats_df, c("id"="ZIPCODE")),
               aes(x=long,
                   y=lat,
                   group=group,
                   fill=POPULATION),
               color="white",
               size=.2) +
  theme_void() +
  coord_map() +
  scale_fill_distiller(palette = "YlGnBu", direction = 1) +
  labs(title="Population in New York City",
       subtitle="Neighborhoods are filled by population",
       fill="Population")
```

Feel free to customize the fill palette, by using bins or other color maps.
For instance here, we used `scale_fill_binned`. More examples can be
seen in the [ggplot2 docs](https://ggplot2.tidyverse.org/reference/scale_colour_continuous.html).

![map_1_binned](/assets/img/articles/maps-ggplot2/map_1_binned.png)

``` R
ggplot() +
  geom_polygon(data=spdf_file %>%
                 inner_join(stats_df, c("id"="ZIPCODE")),
               aes(x=long,
                   y=lat,
                   group=group,
                   fill=POPULATION),
               color="white",
               size=.2) +
  theme_void() +
  coord_map() +
  scale_fill_binned(type = "viridis", direction=-1) +
  labs(title="Population in New York City",
       subtitle="Neighborhoods are filled by population",
       fill="Population")
```

### Draw restaurants as points

We now add a new layer on our maps to show the restaurants, drawn as points.
ggplot2 makes it easy to combine layers, you should find this very intuitive.
Note that the layers order matters. If we add points before polygons, they
will be hidden by the polygons (unless we set a transparent background).

![map_2](/assets/img/articles/maps-ggplot2/map_2.png)

``` R
ggplot() +
  # First layer for counties, as polygons
  geom_polygon(data=spdf_file,
               aes(x=long,
                   y=lat,
                   group=group),
               alpha=0,
               color="black",
               size=.2) +
  # Second layer for restaurants, as points
  geom_point(data=restaurants,
             aes(x=Longitude,
                 y=Latitude),
             fill="red",
             alpha=.6,
             size=3,
             shape=22) +
  theme_void() +
  coord_map() +
  labs(title="Restaurants in New York City")
```

Now we can customize our points, by changing their size and color based on
variables like score and grade.

![map_3](/assets/img/articles/maps-ggplot2/map_3.png)

``` R
ggplot() +
  # First layer for counties, as polygons
  geom_polygon(data=spdf_file,
               aes(x=long,
                   y=lat,
                   group=group),
               alpha=0,
               color="black",
               size=.2) +
  # Second layer for restaurants, as points
  geom_point(data=restaurants,
             aes(x=Longitude,
                 y=Latitude,
                 size=SCORE,   # size according to score
                 fill=GRADE),  # fill according to grade
             alpha=.8,
             shape=22) +
  # Plot settings from here
  theme_void() +
  coord_map() +
  # Edit scale size
  scale_size(limits = c(0, 100)) +
  # Edit fill size with custom colors for grades
  scale_fill_manual(values=c("A"="#2a9d8f",  # custom hex color for grade A
                             "B"="#e9c46a",
                             "C"="#e76f51",
                             "N"="#8ecae6",
                             "Z"="#219ebc"),
                    na.value="grey") +  # custom color for NA values
  # Customize fill legend by increasing the size of the pictograms
  guides(fill=guide_legend(override.aes = list(size = 7))) +
  labs(title="Restaurants in the state of NY",
       subtitle="Sized by score, colored by grade",
       size="Score",
       fill="Grade")
```

### Combine choropleth and points

Now, we combine the previous maps to display both population and restaurants.
It is recommended to avoid putting too much information on maps, as they can
get harder to interpret and the reader might miss the point.
Since we are going to use colors for both counties and restaurants points,
we introduce a very handy command to add a duplicate scale: the
[ggnewscale](https://cran.r-project.org/web/packages/ggnewscale/index.html)
package. We use the line `new_scale("fill")` to tell ggplot we are now using
another fill scale, and show it as a new scale in the legend.

![map_4](/assets/img/articles/maps-ggplot2/map_4.png)

``` R
ggplot() +
  # First layer for counties, as polygons
  geom_polygon(data=spdf_file %>%
                 inner_join(stats_df, c("id"="ZIPCODE")),
               aes(x=long,
                   y=lat,
                   group=group,
                   fill=POPULATION),
               color="white",
               size=.2) +
  # Customize fill for the first layer
  scale_fill_distiller(palette = "YlGnBu", direction = 1) +
  labs(fill="Population") +
  # Add a new fill layer, every fill customization will now apply to the second layer
  new_scale("fill") +
  # Second layer for restaurants, as points
  geom_point(data=restaurants,
             aes(x=Longitude,
                 y=Latitude,
                 size=SCORE,
                 fill=GRADE),
             alpha=.8,
             shape=22) +
  theme_void() +
  coord_map() +
  scale_size(limits = c(0, 100)) +
  # This will customize the second fill layer
  scale_fill_manual(values=c("A"="#2a9d8f",
                             "B"="#e9c46a",
                             "C"="#e76f51",
                             "N"="#8ecae6",
                             "Z"="#219ebc"),
                    na.value="grey") +
  guides(fill=guide_legend(override.aes = list(size = 7))) +
  labs(title="Restaurants in New York City",
       subtitle="Sized by score, colored by grade. With population.",
       size="Score",
       fill="Grade")
```

### Add data from OpenStreetMaps

In this last example, we are going to see how to show data from
[OpenStreetMap](https://www.openstreetmap.org/about), using the
[osmdata](https://cran.r-project.org/web/packages/osmdata/index.html) library.

In the following map, we show subway lines in NYC, colored in red, on top
of the counties.

![map_5](/assets/img/articles/maps-ggplot2/map_5.png)

Let's look at the code to obtain the OpenStreetMap data.

``` R
# Step 1: Bounding box
compute_bbox <- function(restaurants, buffer=.3) {
  restaurants_sf <- st_as_sf(restaurants,
                            coords=c("Longitude", "Latitude"),
                            crs=4326)
  restaurants_sf <- st_transform(restaurants_sf)
  bbox <- st_bbox(st_buffer(restaurants_sf, buffer))

  return(bbox)
}

bbox <- compute_bbox(restaurants)

# Step 2: Retrieve the OpenStreetMap data
osm_railway_for_bbox <- function(bbox, timeout=60) {
  q <- opq(bbox=bbox, timeout=timeout)

  q1 <- add_osm_feature(q, key = "railway", value = "subway")
  subway <- osmdata_sf(q1)$osm_lines

  # add more if you want
  # q2 <- add_osm_feature(q, key = "railway", value = "rail")
  # rail <- osmdata_sf(q2)$osm_lines

  rails <- c(
    st_geometry(subway)
    # st_geometry(rail)  # add more if you want
  )

  return(rails)
}

nyc_railway <- osm_railway_for_bbox(bbox)
```

The first step is to compute a bounding box, which is a rectangle of
coordinates within which we will retrieve the OpenStreetMap data. The function
`compute_bbox` helps us do that, and return the largest bounding box that
contains all our restaurants. The result might look like this:

``` text
     xmin      ymin      xmax      ymax
-74.16900  40.56090 -73.78259  40.87855
```

Then, the function `osm_railway_for_bbox` will return the OpenStreetMap data
we want within the given bounding box. OpenStreetMap has many features with key
values attributes. For instance, the key "railway" has different attributes,
one of which is "subway", defined as "a city passenger rail service". The
full list of values for the key "rail"
[can be found here](https://wiki.openstreetmap.org/wiki/Key:railway).
It's easy to tell which features we want from OpenStreetMap by adding
the following lines of code:

``` R
# get features from the key railway with value = subway.
add_osm_feature(q, key = "railway", value = "subway")
```

Once this data is retrieved within the variable `nyc_railway`, we draw
the map with the following code:

``` R
ggplot() +
  # Layer 1: counties as polygons
  geom_polygon(data=spdf_file,
               aes(x=long,
                   y=lat,
                   group=group),
               alpha=0,
               color="black",
               size=.2) +
  # Layer 2: add the retrieved data from OpenStreetMap
  geom_sf(data=nyc_railway,
          size=.3,
          alpha=1,
          color="red") +
  theme_void() +
  # Coordinates system should be sf now
  coord_sf() +
  labs(title="Railway from OpenStreetMaps",
       subtitle="Showing subway and rail")
```

## Conclusion

I hope this post was useful. You can find the full code in this
Github repository: [github.com/ericdaat/maps-R-ggplot2](https://github.com/ericdaat/maps-R-ggplot2).
Let me know if you have any questions in the comments, or if there is
anything wrong with my code.
