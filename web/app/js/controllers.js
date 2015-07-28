var domotekControllers = angular.module('domotekControllers', ['ngMaterial']);
domotekControllers.controller('MainCtrl', ['$scope','Controller',
 function($scope,Controller) {
	$scope.controllers = Controller.query();
    $scope.tagline = 'To the moon and back!';   

}]);
// Controlleurs
domotekControllers.controller('ControllerCtrl', ['$scope','$routeParams', 'Controller',
  function($scope, $routeParams,Controller) {

	$scope.controllers = Controller.get({id: $routeParams.id});
      var updateController= function(status){
          $scope.controllers.forEach(function(controller){
              console.log("updating controller "+controller.name);
              controller.status = status;
              Controller.put({id:controller.id},controller);
          });
      }
    console.log($scope);
       $scope.$watch('controller.status',function(newVal,oldVal){
           if(oldVal != newVal){
            console.log("had :"+oldVal);
           console.log("got :"+newVal);
           updateController(newVal)
           }
       });
      $scope.clickController= function (){
        $scope.controllers.forEach(function(controller){
            Controller.switchIt({id:controller.id},controller)
      })
    }

}]);
// Elements
domotekControllers.controller('ElementCtrl', ['$scope','$routeParams', 'Element',
  function($scope, $routeParams,Element) {

	$scope.elements = Element.get({id: $routeParams.id});
      var updateElement= function(status){
          $scope.elements.forEach(function(element){
              console.log("updating Element "+element.name);
              element.status = status;
              Element.put({id:element.id},element);
          });
      }
    console.log($scope);
       $scope.$watch('element.status',function(newVal,oldVal){
           if(oldVal != newVal){
            console.log("had :"+oldVal);
           console.log("got :"+newVal);
           updateElement(newVal)
           }
       });
      $scope.clickController= function (){
        $scope.elements.forEach(function(element){
            Element.switchIt({id:element.id},element)
      })
    }

}]);