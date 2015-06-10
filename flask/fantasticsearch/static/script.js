$(document).ready(function() {
	var checkboxes = document.getElementsByClassName('checkbox');
	for (i = 0; i < checkboxes.length; i++){
		var checkbox = checkboxes[i];
		checkbox.getElementsByTagName('input')[0].addEventListener('click', getFilters, false);
	}
});



function getFiltersFromDom(){
	var filters = [];
	
	var checkboxes = document.getElementsByClassName('checkbox');
	for (i = 0; i < checkboxes.length; i++){
		var checkbox = checkboxes[i];
		var input = checkbox.getElementsByTagName('input')[0];
		if (input.checked == true){
			filters.push(input.id);
		}
	}

	return filters;	
};



function getFilters() {
	var checkbox = this;
	var term =  getURLParameter('term');		
	var id = checkbox.id;

	var filters = getFiltersFromDom();
	
	if (checkbox.checked == true){
		filters.push(id);
		var url = '/search?term='+term+'&filter='+filters;
		$.get(url, function (response) {
			document.open();
			document.write(response);
			document.close();
			toggleAllFilters(filters);
		});
	} else {		
		var url = '/search?term='+term+'&filter='+filters;
		$.get(url, function (response) {
			document.open();
			document.write(response);
			document.close();
			toggleAllFiltersBut(id, filters);
		});
	}
};



function toggleAllFilters(filters) {

	for (i = 0; i < filters.length; i++){
		var filter = filters[i];
		document.getElementById(filter).checked = true;
	}
};


function toggleAllFiltersBut(id, filters) {
	
	document.getElementById(id).checked = false;

	for (i = 0; i < filters.length; i++){
		var filter = filters[i];
		if (filter !== id) {
			document.getElementById(filter).checked = true;
		} 
	}
};


function getURLParameter(name) {
  	return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
}
