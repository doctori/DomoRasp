'use strict';
var DomoRasp = angular.module('DomoRasp', [
	'ngRoute',
	'ngMaterial',
	'domotekControllers',
	'domotekServices'
	]);
	
	DomoRasp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
            templateUrl: 'views/home.html',
            controller: 'MainCtrl'
        }).
      when('/controllers/:id', {
            templateUrl: 'views/controllers.html',
            controller: 'ControllerCtrl'
        }).
        when('/elements/:id',{
            templateUrl: 'views/elements.html',
            controller: 'ElementCtrl'
        }).
      otherwise({
        redirectTo: '/'
      });
  }]);