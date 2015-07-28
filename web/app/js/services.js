var domotekServices = angular.module('domotekServices', ['ngResource'])
domotekServices.factory('Controller',
	function($resource) {
        console.log($resource);
	return 	$resource('/api/controllers/:id/:action',{},{
		get:{isArray:true},
        put: { method: 'PUT',isArray:false},
        switchIt:{method: 'GET',isArray:false,params:{action:'switch'}}
	});
});
domotekServices.factory('Element',
	function($resource) {
        console.log($resource);
	return 	$resource('/api/elements/:id/:action',{},{
		get:{isArray:true},
        put: { method: 'PUT',isArray:false},
        switchIt:{method: 'GET',isArray:false,params:{action:'switch'}}
	});
});
