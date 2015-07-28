// public/js/appRoutes.js
    angular.module('appRoutes', []).config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

    $routeProvider

        // home page
        .when('/', {
            templateUrl: 'views/home.html',
            controller: 'MainCtrl'
        })

        // controlers page that will use the ControlerController
        .when('/controllers', {
            templateUrl: 'views/controllers.html',
            controller: 'ControllerCtrl'
        });

    $locationProvider.html5Mode(true);

}]);