//  Calling the renderHTML function
//renderHTML();

// Getting a reference to the element on the page with an ID of app
// Plot the default route once the page loads
var default_url = "/samples/BB_940";
var selectDropdown = document.querySelector("#selDataset");
Plotly.d3.json(default_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    var layout = { margin: { t: 30, b:100 } }
    Plotly.plot("line", data, layout)
})

// Update the plot with new data
function updatePlotly(newdata) {
    var Line = document.getElementById('line');
    Plotly.restyle(Line, "OTU_IDS", [newdata.OTU_IDS])
    Plotly.restyle(Line, "SAMPLE_VALUES", [newdata.SAMPLE_VALUES])
}

// Get new data whenever the dropdown selection changes
function getData(route) {
    console.log(route);
    Plotly.d3.json(`/${route}`, function(error, data) {
        console.log("newdata", data);
        updatePlotly(data);
    });
}
var names_url = "/names";
Plotly.d3.json(names_url, function(error, results) {
    if (error) return console.warn(error);
    var names = [results];
    for (var i=0;i<names.length-1;i++) {
        //convert this section to add <option value="samples/BB_XXX"> BB_XXX </option> for each sample name in the dropdown
        //current error is that I cannot input a value for each specific link into the option tag using createElement, but
        //I also do not expect a pure text append for string: "<option value="samples/BB_XXX"> BB_XXX </option>" to be able 
        //To recognize that the samples/BB_XXX value changes
        var dropdownName = String(names[i]);
        var dropdownLink = "samples/"+dropdownName
        var dropdownValue = document.createElement("option").setAttribute("value", dropdownLink);
        dropdownValue.innerHTML = dropdownName;
        selectDropdown.appendChild(dropdownValue);
      }
})        

