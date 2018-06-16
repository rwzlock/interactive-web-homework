//Javascript file with identical code to the script found in the html file
var default_url = "/samples/BB_941";
        //Plot the bar graph with the top ten otu_ids by value for the default sample (BB_941)
        Plotly.d3.json(default_url, function(error, response) {
            if (error) return console.warn(error);
            var data = [response];
            console.log(data)
            var layout = { margin: { t: 30, b:100 },
                           title: "Top 10 Otu IDS by Sample",
                           xaxis: { title: "Otu ID"},
                           yaxis: { title: "Value"}            
            }
            Plotly.plot("bar", data, layout)
        })

        // Update the plot with new data (occurs when a different sample is selected in the dropdown)
        function updatePlotly(newdata) {
            var Bar = document.getElementById('bar');
            Plotly.restyle(Bar, "x", [newdata.x])
            Plotly.restyle(Bar, "y", [newdata.y])
        }

        // Get new data whenever the dropdown selection changes
        function getData(route) {
            console.log(route);
            Plotly.d3.json(`/${route}`, function(error, data) {
                console.log("newdata", data);
                updatePlotly(data);
        });
        }
        //Code to recreate the dropdown menu with values defined by columns in the samples table (Does not work)
        var selectDropdown = document.querySelector("#selDataset");
        var names_url = "/names";
        Plotly.d3.json(names_url, function(error, response) {
            if (error) return console.warn(error);
            var names = [response];
            console.log(names)
            console.log(names.length)
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