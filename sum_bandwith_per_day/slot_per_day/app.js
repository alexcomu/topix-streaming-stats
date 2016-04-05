/**
 * Created by alexcomu on 04/04/16.
 */
angular.module("comuapp",[])

    .controller("ComuCtrl", function($scope, $http){

        $scope.initPage = function(){
            $scope.year_choice = "2012";
            $scope.app_choice="ALL";
            $scope.changeChoice();
        };

        $scope.changeChoice = function(){
            $scope.view_message = "Viewing year "+$scope.year_choice;
            if($scope.app_choice=="ALL"){
                url = "/result/aggregated_"+$scope.year_choice+"_perslot.json";
                $scope.view_message+=" for all aggregated apps";
            }
            else{
                url = "/result/aggregated_"+$scope.year_choice+"_result_"+$scope.app_choice+".json";
                if($scope.app_choice=="rt"){
                    $scope.view_message += " for RED CARPET";
                }else if($scope.app_choice=="pk"){
                    $scope.view_message += " for PRESS CONFERENCE";
                }else{
                    $scope.view_message += " for BERLINALE FILM";
                }
            }

            $http.get(url).success(function(result){
                $scope.result = result;
                $scope.loading = false;
            });
        }
    });