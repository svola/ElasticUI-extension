var app = angular.module('demo', ['elasticui', 'elif']);

app.constant('euiHost', 'http://localhost:9200');  <!-- TODO: change to your host-->
app.controller('IndexController', function($scope) {
    $scope.indexName = "INDEX_NAME"; <!--TODO: change to your index-name -->
});

