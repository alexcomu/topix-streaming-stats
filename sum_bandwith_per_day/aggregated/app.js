/**
 * Created by alexcomu on 04/04/16.
 */
angular.module("comuapp",[])

    .controller("ComuCtrl", function($scope, $http){

        $scope.initPage = function(){
            $scope.choice = "2012";
            $scope.changeChoice();
        };

        $scope.changeChoice = function(){
            $http.get("/aggregated_"+$scope.choice+"_perslot.json").success(function(result){
                $scope.result = result;
                $scope.loading = false;
            });
        }
    });