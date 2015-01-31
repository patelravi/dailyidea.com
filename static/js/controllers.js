var dailyIdeaControllers = angular.module("dailyIdeaControllers", []);

dailyIdeaControllers.controller("StaticPageCtrl", function($scope, $location) {
    $scope.getClass = function(path) {
        if ($location.path() == path) {
          return "pure-menu-selected"
        } else {
          return ""
        }
    }
});

dailyIdeaControllers.controller("IdeaListCtrl", function($scope, $http) {
    var api_endpoint = "/api/ideas/";
    var url = base_url + api_endpoint;
    $http.get(url).success(function(data) {
        $scope.ideas = data.hits.hits;
    });
});

dailyIdeaControllers.controller("IdeaDetailCtrl", function($scope, $routeParams, $http) {
    $scope.ideaID = $routeParams.ideaID;
    var api_endpoint = "/api/ideas/" + $routeParams.ideaID + "/";
    var url = base_url + api_endpoint;
    $http.get(url).success(function(data) {
        $scope.idea = data;
    });
});

dailyIdeaControllers.controller("CreateIdeaCtrl", function($scope, $http) {
    $scope.submit = function() {
        var api_endpoint = "/api/ideas/new/";
        var url = base_url + api_endpoint;
        $http.post(url, $scope.ideaForm)
            .success(function(data, status, headers, config) {
                console.log("Success:", data, status, headers, config);
            })
    };
});

dailyIdeaControllers.controller("UserDetailCtrl", function($scope, $routeParams, $http) {
    $scope.username = $routeParams.username;
    var api_endpoint = "/api/users/" + $routeParams.username + "/";
    var url = base_url + api_endpoint;
    $http.get(url).success(function(data) {
        $scope.ideas = data.hits.hits;
    });
});
