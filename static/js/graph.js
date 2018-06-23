queue()
    .defer(d3.json, "/worldStats/worldCountries")
    .await(makeGraphs);

function makeGraphs(error, donorsUSProjects) {
    if (error) {
        console.error("makeGraphs error on receiving dataset:", error.statusText);
        throw error;
    }



    //Create a Crossfilter instance
    var cf = crossfilter(donorsUSProjects);

    //Define Dimensions//
    var resourceTypeDim = cf.dimension(function (d) {
        return d["languages"];},true);
    var currencyStatus = cf.dimension(function (d) {
        return d["currency"];},true);
    var continentStatus = cf.dimension(function (d) {
        return d["continent"];});
    var countryDim = cf.dimension(function(d) {
        return d["country"];});
    var driveDim = cf.dimension(function(d) {
        return d["drive"];});


    //Calculate metrics
    var ContinentStatusGroup = continentStatus.group();
    var driveGroup = driveDim.group();
    var fullCurrencyStatus = currencyStatus.group();
    var numProjectsByResourceType = resourceTypeDim.group();
    var sumGroup = countryDim.group().reduceSum(function(d) {
        return d["population"];
    });
    var ContinentPopGroup = continentStatus.group().reduceSum(function(d) {
        return d["population"];
    });

    var all = cf.groupAll();

    var totalDonations = cf.groupAll().reduceSum(function (d) {
        return d["population"];
    });
    var totalArea = cf.groupAll().reduceSum(function (d) {
        return d["area"];
    });


    //Charts
    var continentStatusChart = dc.pieChart("#continent-chart");
    var currencyChart = dc.rowChart("#currency-chart");
    var areaChart = dc.numberDisplay("#total-area");
    var totalPopulation = dc.numberDisplay("#total-population");
    var selectField = dc.selectMenu('#menu-select');
    var numberCountries = dc.numberDisplay("#numberCountries");
    var populationChart = dc.barChart('#Population-Bar-Chart');
    var languageChart = dc.rowChart("#languages-row-chart");
    var countriesChart = dc.rowChart("#country-chart");
    var fullresults = dc.dataTable("#FullResultsTable");
    var driveChart = dc.pieChart("#drive-chart");



    continentStatusChart
        .ordinalColors(["#79CED7", "#66AFB2", "#C96A23"])
        .width(300)
        .height(300)
        .radius(150)
        .innerRadius(50)
        .transitionDuration(1500)
        .group(ContinentStatusGroup)
        .dimension(continentStatus);

    currencyChart
        .ordinalColors(["#79CED7", "#66AFB2", "#C96A23", "#D3D1C5", "#F5821F"])
        .width(300)
        .height(300)
        .margins({top: 0, right: 10, bottom: 20, left: 10})
        .cap(10)
        .elasticX(true)
        .dimension(currencyStatus)
        .group(fullCurrencyStatus)
        .ordering(function(d){
            return -d.value;
        })
        .xAxis().ticks(3);

    areaChart
        .formatNumber(d3.format("d"))
        .valueAccessor(function (d) {
            return d;
        })
        .group(totalArea)
        .formatNumber(d3.format(",.2r"));

    totalPopulation
        .formatNumber(d3.format("d"))
        .valueAccessor(function (d) {
            return d;
        })
        .group(totalDonations)
        .formatNumber(d3.format(",.2r"));

    selectField
        .group(sumGroup)
        .dimension(countryDim);

    numberCountries
        .formatNumber(d3.format("d"))
        .valueAccessor(function (d) {
            return d;
        })
        .group(all);

    countriesChart
        .ordinalColors(["#79CED7", "#66AFB2", "#C96A23", "#D3D1C5", "#F5821F"])
        .width(750)
        .height(460)
        .group(sumGroup)
        .dimension(countryDim)
        .renderLabel(true)
        .elasticX(true)
        .ordering(function(d){
            return -d.value;
        })
        .cap(30)
        .xAxis().tickFormat(function (v) {
            return v /10000000 +"M";
        });

    populationChart
        .ordinalColors(["#79CED7", "#66AFB2", "#C96A23", "#D3D1C5", "#F5821F"])
        .width(500)
        .height(200)
        .ordering(function(d){
            return d.value;
        })
        .outerPadding(0)
        .gap(0.5)
        .margins({top: 10, right: 10, bottom: 20, left: 40})
        .group(ContinentPopGroup)
        .dimension(continentStatus)
        .elasticY(true)
        .xUnits(dc.units.ordinal)
        .brushOn(false)
        .x(d3.scale.ordinal().range(donorsUSProjects.length))
        .renderHorizontalGridLines(true)
        .yAxis().ticks(10).tickFormat(d3.format('.3s'));

    languageChart
        .ordinalColors(["#33CC99"])
        .renderLabel(true)
        .width(300)
        .height(200)
        .ordering(function(d){
            return -d.value;
        })
        .group(numProjectsByResourceType)
        .cap(10)
        .othersGrouper(false)
        .elasticX(true)
        .dimension(resourceTypeDim)
        .xAxis().ticks(10);

    fullresults
        .dimension(countryDim)
        .group(function (d) {
            return '';
        })
        .size(236)
        // create the columns dynamically
        .columns([
            {
                label: "Country",
                format: function (d) {return  d.country}
            },
            {
                label: "Capital",
                format: function (d) {return d.capital}
            }
            ])
        .sortBy(function (d) {
            return d.country})
        .order(d3.ascending);

    driveChart
        .ordinalColors(["#66AFB2", "#C96A23"])
        .width(200)
        .height(200)
        .radius(100)
        .innerRadius(30)
        .transitionDuration(1500)
        .group(driveGroup)
        .dimension(driveDim);

    // Render all Charts
    dc.renderAll();
}