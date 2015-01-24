var dailyIdeaControllers = angular.module("dailyIdeaControllers", []);

dailyIdeaControllers.controller("IdeaListCtrl", function($scope, $http) {
    var api_endpoint = "/api/ideas/"
    var url = base_url + api_endpoint
    $http.get(url).success(function(data) {
        $scope.ideas = data.hits.hits;
    });
});

dailyIdeaControllers.controller("IdeaDetailCtrl", function($scope, $routeParams, $http) {
    $scope.ideaID = $routeParams.ideaID;
    var api_endpoint = "/api/ideas/" + $routeParams.ideaID + "/";
    // es.search(index="main",body={"query":{"match":{"_id":"AUskBJjhBhfpAnqYEubn"}}})['hits']['hits'][0]
    var url = base_url + api_endpoint
    $http.get(url).success(function(data) {
        $scope.idea = data;
        console.log(data);
    });
});

dailyIdeaControllers.controller("CreateIdeaCtrl", function($scope, $http) {
    $scope.submit = function() {
        var api_endpoint = "/api/ideas/new/"
        var url = base_url + api_endpoint
        $http.post(url, $scope.ideaForm)
            .success(function(data, status, headers, config) {
                console.log("Success:", data, status, headers, config);
            })
    };
});

