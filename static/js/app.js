var base_url = ""

var dailyIdeaApp = angular.module("dailyIdeaApp", [
    'ngRoute',
    'ngSanitize',
    'angularMoment',
    'dailyIdeaControllers',
]);

dailyIdeaApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/html/partials/landing.html',
                controller: 'StaticPageCtrl'
            }).
            when('/inspiration', {
                templateUrl: '/static/html/partials/inspiration.html',
                controller: 'StaticPageCtrl'
            }).
            when('/features', {
                templateUrl: '/static/html/partials/features.html',
                controller: 'StaticPageCtrl'
            }).
            when('/ideas', {
                templateUrl: '/static/html/partials/idea_list.html',
                controller: 'IdeaListCtrl'
            }).
            when('/ideas/new', {
                templateUrl: '/static/html/partials/create_idea.html',
                controller: 'CreateIdeaCtrl'
            }).
            when('/ideas/:ideaID', {
                templateUrl: '/static/html/partials/idea_detail.html',
                controller: 'IdeaDetailCtrl'
            }).
            when('/users/:username', {
                templateUrl: '/static/html/partials/user_detail.html',
                controller: 'UserDetailCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
    }
]);
