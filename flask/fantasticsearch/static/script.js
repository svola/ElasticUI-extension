$(document).ready(function() {
	var checkboxes = document.getElementsByClassName('checkbox');
	for (i = 0; i < checkboxes.length; i++){
		var checkbox = checkboxes[i];
		checkbox.getElementsByTagName('input')[0].addEventListener('click', getFilters, false);
	}
});


function getFilters() {
	var checkbox = this;
	var term =  getURLParameter('term');		
	var id = checkbox.id;

	var filterSession = sessionStorage.getItem("filters");
	if (filterSession){	
		var filters = filterSession.split(',');
	} else {
		var filters = [];
	}
	
	if (checkbox.checked == true){
		var index = filters.indexOf(id);
		if (index == -1) {
    			filters.push(id);
		}
		sessionStorage.setItem("filters", filters);

		var url = '/search?term='+term+'&filter='+filters;
		$.get(url, function (response) {
			document.open();
			document.write(response);
			document.close();
			toggleAllFilters();
		});
	} else {
		var index = filters.indexOf(id);
		if (index > -1) {
    			filters.splice(index, 1);
		}
		sessionStorage.setItem("filters", filters);

		var url = '/search?term='+term+'&filter='+filters;
		$.get(url, function (response) {
			document.open();
			document.write(response);
			document.close();
			togglleAllFiltersBut(id);
		});
	}
};



function toggleAllFilters() {
	var filterSession = sessionStorage.getItem("filters");
	if (filterSession){	
		var filters = filterSession.split(',');
	} else {
		var filters = [];
	}

	for (i = 0; i < filters.length; i++){
		var filter = filters[i];
		document.getElementById(filter).checked = true;
	}
};


function toggleAllFiltersBut(id) {
	var filterSession = sessionStorage.getItem("filters");
	if (filterSession){	
		var filters = filterSession.split(',');
	} else {
		var filters = [];
	}

	
	for (i = 0; i < filters.length; i++){
		var filter = filters[i];
		if (filter !== id) {
			document.getElementById(filter).checked = true;
		} else {
			document.getElementById(id).checked = false;
		}
	}
};


function getURLParameter(name) {
  	return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
}
