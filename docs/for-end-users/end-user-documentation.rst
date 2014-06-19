End users documentation for DaViz
=================================

Introduction
++++++++++++
EEA Daviz is a web tool developed by the European Environment Agency which helps creating interactive data visualizations easily through the web browser, no extra tools are necessary. It is free and open source.

You can generate attractive and interactive charts and combine them in a dashboard with facets/filters which updates the charts simultaneously. Data can be uploaded as CSV/TSV or you can specify SPARQL to query online Linked open data servers (aka sparql endpoints).

Daviz is the first Semantic web data visualisation tool for Plone CMS, entirely web-based!
At the moment Simile Exhibit and Google Charts visualizations are supported.

1. Add a data source
++++++++++++++++++++
When you are starting to create a visualization, the first step is to set the data source for it.
First, add a Data Visualization. On the edit page you have several options to set the data source:

    - copy/paste: you can copy the data from an excel file, a tsv or csv file or another website.

        video: https://www.youtube.com/watch?v=ahxHks8-Fkc

    - csv/tsv upload: you can upload a csv or tsv file, and use it as datasource:

        video: https://www.youtube.com/watch?v=myFn3zmvpQI

        demo: http://daviz.eionet.europa.eu/learn-more/visualisations-examples/basic-tutorials/daviz-from-csv

    - via url/json: you can use an external url what points to a json.

        video: https://www.youtube.com/watch?v=P2v_uzVl14U

        demo: http://daviz.eionet.europa.eu/learn-more/visualisations-examples/basic-tutorials/daviz-from-url

    - from another DaViz: you can use an existing DaViz and reuse the same data.

        video: https://www.youtube.com/watch?v=iqyU04fzz_8

        demo: http://daviz.eionet.europa.eu/learn-more/visualisations-examples/basic-tutorials/daviz-from-existing-daviz

    - sparql: you can create your own sparql query and use it as data source for your visualization.

        video: https://www.youtube.com/watch?v=2Qn48OTDtxY

        demo: http://daviz.eionet.europa.eu/learn-more/visualisations-examples/basic-tutorials/daviz-from-sparql-query

If you are ready, hit the Save button, and you will be redirected to the Edit Visualization page where the default Table chart is created.

2. Data settings
++++++++++++++++
After you have your datasource selected and created your new DaViz, on the Edit Visualization page on the Data Settings tab you can make some customization for the data, like setting some friendly names to the columns and forcing the type for values on a column.
These settings are applied on all google charts and exhibit views inside this DaViz.

3. Exhibit visualizations
+++++++++++++++++++++++++
Using the exhibit visualizations you can enable map, tabular, timeline and tile views. You can have only one of each type of view enabled for a visualization.

First you have to enable them. For this, on the Edit Visualization page select one of the exhibit views from the tab, and press the Enable View button.

3.1 Available exhibit visualizations:
-------------------------------------

3.1.1 Map view
^^^^^^^^^^^^^^
Requires **latitude** and **longitude** columns (this can be in a single column or separate ones). After enabling this view you have to select which column(s) stores the coordonates.

    video: https://www.youtube.com/watch?v=aIKXHokacsQ

3.1.2 Timeline view
^^^^^^^^^^^^^^^^^^^
Requires start date and end date columns. For this view you have to select which column stores the start date and which column the end date.

    video: https://www.youtube.com/watch?v=17yDtMUJaOc#t=20

3.1.3 Tabular view
^^^^^^^^^^^^^^^^^^
Has no data constraints. On this view you have to select which columns to be displayed. 

    video: https://www.youtube.com/watch?v=WJF4tPG9r_o

3.1.4 Tile view
^^^^^^^^^^^^^^^
has no data constraints. This view doesn't require any configuration.

    video: https://www.youtube.com/watch?v=YuZclux0-aI

3.4 Advanced settings
---------------------
For each exhibit view you can access the advanced settings, where you can finetune the view.

    video: https://www.youtube.com/watch?v=eN4dlo3zepc

    demo: http://daviz.eionet.europa.eu/learn-more/visualisations-examples/advanced-tutorials/exhibit-charts

3.2 Simile Lens
---------------
On each view you have the possibility to customize how the data from a row to be displayed. This is done using the Lens template.

    exhibit lens doc: http://www.simile-widgets.org/wiki/Exhibit/Lens_Templates

    video: https://www.youtube.com/watch?v=0Z_lRNfQj4Y

3.3 Facets
----------
Facets are used to filter your data. Exhibit facets are shared between all your exhibit views, they will appear on all of them and preserve the selected values.

    video: https://www.youtube.com/watch?v=zA_OZ0zxWAI

4. Google Charts
++++++++++++++++
DaViz is using Googlecharts to display charts. The configurator is based a customized google chart editor, allowing to create various charts based on the same data source.

To be able to create google charts on the Edit Visualization page go to the Charts tab. As one DaViz may contain several charts, you can add them by clicking on the **Add another visualization** https://www.youtube.com/watch?v=Qg6algUSjz8

You can have as many different charts, what you can customize independently, add filters and notes. You can also reorder them, or hide them.

    video: https://www.youtube.com/watch?v=gz6fhA9lttE

After you added a new chart, you can specify it's title, and start to customize it.

For customizing, click on the **Edit** button of the chart, this will open a dialog with the **Chart Eeditor**.

4.1 Chart Editor:
-----------------
The **Chart Editor** is based on google charts built in chart editor highly customized, with features like: data manipulation, color palette, setting roles for columns.

The **Chart Editor** has two main features selecting the chart and customizing it (this can be done on the **Chart** tab) and preparing/modifying in order to need the required structure for the chart (on the **Data selection for chart**).

In case your data fits the chart you want to create you don't have to make modifications on the data and the chart will display after selecting it from the list of the charts. Otherwise you will get an error message and you will have to hide/reorder/pivot/unpivot the columns until you will get the structure that fits the chart.

4.1.1 Selecting the chart
^^^^^^^^^^^^^^^^^^^^^^^^^
In the **Chart Editor** dialog you can select one of the following type of charts, but all of them requires different format for the data

        video: https://www.youtube.com/watch?v=WmPVatF6kh8

    - Line charts:

        The first column should contain the category label. Data values should appear as numeric columns. Each numeric column may be followed by one or two text columns. The text in the first column will be displayed as annotations above the data points. The text in the second column will be displayed in a hover-card when hovering over the point.

        video: https://www.youtube.com/watch?v=z_redV-Qxto

    - Combo charts

        The first column should contain the category label. Any number of columns can follow, all should be numeric.

    - Area charts

        The first column should contain the category label. Data values should appear as numeric columns. Each numeric column may be followed by one or two text columns. The text in the first column will be displayed as annotations above the data points. The text in the second column will be displayed in a hover-card when hovering over the point.

    - Stepped area chart

        The first column should contain the category label. Any number of columns can follow, all must be numeric. Each column is displayed as a separate line.

    - Column charts

        The first column in the table represents the label of a group of bars. Any number of columns can follow, all numeric, each representing the bars with the same color and relative position in each group. The value at a given row and column determines the height of the single bar represented by this row and column.

        video: https://www.youtube.com/watch?v=WZkneabgDxY

    - Histograms

        A histogram displays the distribution of a data set. The first column in the table represents the label of a group of data. Any number of columns can follow, all numeric, each representing items in a distribution. For each column, the values from all rows are grouped into numeric buckets. The histogram displays the number of values in each bucket, using the height of each bar to represent the count of values.

    - Bar charts

        The first column in the table represents the label of a group of bars. Any number of columns can follow, all numeric, each representing the bars with the same color and relative position in each group. The value at a given row and column determines the height of the single bar represented by this row and column.

        video: https://www.youtube.com/watch?v=Qg6algUSjz8

    - Scatter charts

        Two or more columns are required, all must be numeric. The values in the first column are used for the X-axis. The values in following columns are used for the Y-axis. Each column is displayed with a separate color.

    - Bubble charts

        The first column in the table should be text, and represents the label of that bubble. The numbers in the second column are plotted on the x axis. The numbers in the third column are plotted on the y axis. The optional fourth column should be text, and determines the bubble color. The optional fifth column is numeric, and determines the size of the bubble.

    - Pie charts

        The first column should contain the slice label. The second column should be a number, and contain the slice value.

        video: https://www.youtube.com/watch?v=LWDCzetUs80

    - Geo charts

        The first column should contain location names or addresses. The second column should contain numeric values.

        video: https://www.youtube.com/watch?v=WuL9jUBVbr8

    - Spark lines

        All columns must be numeric.

    - Time line

        The first column should contain dates. Subsequently, all columns should contain numbers or text. Each numeric column may be followed by one or two text columns.

    - Motion chart

        The first column should contain entities (e.g. countries) the second is time (e.g. years) followed by 2-4 numeric or string columns.

    - Candlestick chart

        The first column should be the names of the stocks or categories. The second column represents the low or minimum value for the stock or category, the third columnepresents the opening or initial value for the stock or category, the fourth column represents the closing or final value for the stock or category, and the fifth column represents the high or maximum value for the stock or category. The optional sixth column contains tooltip text.

    - Gauge

        The first column should be the label text for the gauge. The second column should be the gauge value.

    - Organizational chart

        The first column is the name of an individual in the chart. The second column is the name of the individual's parent or manager. The optional third column is tooltip text.

    - Tree map

        The first column should be the name of an entity in a hierarchy. Each entity is visualized by a box when the chart is rendered. The second column should be the name of the entity's parent entity. (The value in the second column of each row should be found in the first column of some other row.) The optional third and fourth columns should be numerical values associated with the entity. The third column is visualized as the size of the box (must be a positive number), and the fourth column is visualized as the color of the box (may be a negative number).

    - Table


4.1.2 Data Selection for chart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If your data doesn't fit the selected chart, you have to make some adjustments to it on the **Data selection for chart** - tab

On this section you can:

    - unpivot the table, transform columns to rows

        video: https://www.youtube.com/watch?v=iizABOyCw7Q

    - pivot the table, transform rows to columns

        video: https://www.youtube.com/watch?v=7WYz-SJpbNk

    - reorder the columns
    - hide columns from the table

        video: https://www.youtube.com/watch?v=tWJPJSjk4_U

    - sort data in the table
    - hide rows from the table

        video: https://www.youtube.com/watch?v=RKkxcIhkWoo

    - format the values of a column

        video: https://www.youtube.com/watch?v=iEkZfuS9iFc

    - set a role for a column:

        - data
        - old data
        - interval
        - annotation
        - annotationText
        - tooltip
        - certainty
        - emphasis
        - scope

    - set a custom tooltip for a column
    - using the Scatterplots matrix and the other matrices you can quickly search for relations in the data and select the columns for the chart

        videos:

            https://www.youtube.com/watch?v=NEkUe2DK4pA

            https://www.youtube.com/watch?v=dxahseQj2NM

4.1.3 Customize charts
^^^^^^^^^^^^^^^^^^^^^^
You can improve the look of the chart by customizing it. Depending on the selected chart, you have a big number of configuration options, like: color palette, legend, lines/bar/columns width, horizontal and vertical axes label and layout, point shape and sizes, trendlines, intervals etc.

    videos:

        https://www.youtube.com/watch?v=2gal_jMet-A

        https://www.youtube.com/watch?v=PitVnPON1zo

        https://www.youtube.com/watch?v=u_XxJrROHic

        https://www.youtube.com/watch?v=qYpNkzgLd6k

When the chart is ready, press the **Save** button on the dialog.

4.2 Preview and size adjustments
--------------------------------
By default all charts have a size of 800x600px. If you want to modify this, you have to click on "Preview and size adjusments" what will open a dialog with the final version of the chart. Here, with drag and drop you can simply resize the chart (or type in the prefered values in the text fields).

4.3 Filters, Sorting, Notes
---------------------------
When the chart is ready, you can add to it filters, sorting options and notes.

    video: https://www.youtube.com/watch?v=plHtVyIkQuA

4.4 Dashboards
--------------
Dashboards are collections of charts. From the already created charts you can simply add the charts to your dashboard, resize them and place them in positions. You can also add portlets, rich text fields and filters to a dashboard.

    video: https://www.youtube.com/watch?v=xXuHL13pX08

4.5 Embedding charts
--------------------
You have several possibilities to embed your charts on other pages:

    - simple embed in an iframe

        video: https://www.youtube.com/watch?v=UfKXd4-TcHE

            When normal embed is used you have a few customization possibilities:

        - customize it's css

            video: https://www.youtube.com/watch?v=ojiwiSxM-FM

        - configure if the filters should preserve their values and if the filters should be displayed or not

            video:  https://www.youtube.com/watch?v=WN6O9fOyZdI

    - embed static images (snapshots of the charts)

        video: https://www.youtube.com/watch?v=KI9_vQSQy5U

    - embed them in indicators

        video: https://www.youtube.com/watch?v=hcEhSjqHjWE

