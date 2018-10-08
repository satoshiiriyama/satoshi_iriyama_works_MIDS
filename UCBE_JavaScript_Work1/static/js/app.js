// from data.js
var tableData = data;

// YOUR CODE HERE!
var tbody = d3.select("tbody");

tableData.forEach(function(ufoData) {
    console.log(ufoData);
    var row = tbody.append("tr");
    Object.entries(ufoData).forEach(function([key, value]) {
        console.log(key, value);
        var cell = tbody.append("td");
        cell.text(value);
    });
});


var filterButton = d3.select("#filter-btn");
var inputFieldDate = d3.select("#datetime");
var inputFieldCity = d3.select("#city");
var inputFieldState = d3.select("#state");
var inputFieldCountry = d3.select("#country");
var inputFieldShape = d3.select("#shape");


filterButton.on("click", function() {
    d3.event.preventDefault();

    tbody.html("")

    var inputDate = inputFieldDate.property("value");
    var inputCity = inputFieldCity.property("value");
    var inputState = inputFieldState.property("value");
    var inputCountry = inputFieldCountry.property("value");
    var inputShape = inputFieldShape.property("value");
   
    console.log(inputDate);

    tableData.forEach(function(ufoData) {
        if ((inputDate ==="" || ufoData.datetime === inputDate) && 
            (inputCity ==="" || ufoData.city.toUpperCase() === inputCity.toUpperCase()) && 
            (inputState ==="" || ufoData.state.toUpperCase() === inputState.toUpperCase()) && 
            (inputCountry ==="" || ufoData.country.toUpperCase() === inputCountry.toUpperCase()) && 
            (inputShape ==="" || ufoData.shape.toUpperCase() === inputShape.toUpperCase())) {
            console.log(ufoData);
            var row = tbody.append("tr");
            Object.entries(ufoData).forEach(function([key, value]) {
                console.log(key, value);
                var cell = tbody.append("td");
                cell.text(value);
            });
        }
    })
});
    
