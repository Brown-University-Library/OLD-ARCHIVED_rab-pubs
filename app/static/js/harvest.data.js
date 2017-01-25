harvest.data = (function () {

	var
		configMap = {
			resource_base : "http://vivo.brown.edu/individual/",
			api_base : null
		},

		initModule, configModule;

	configModule = function ( config ) {
		configMap.api_base = config.api_base;
	};

	initModule = function ( shortid ){

          (function() {
            var target = '#1b404f6f24b449688bed96f0b2587d4d-pending-collapse';
            var count = $(target).data('pending-count');
            if (count > 0) {
              $.ajax({
                dataType: "json",
                crossDomain: true,
                url: 'http://localhost:8000/rabpubs/' + shortid + '/pending/pubmed',
                success: function( data ) {
                  var source = '1b404f6f24b449688bed96f0b2587d4d';
                  harvest.model.update( data, source );
                  $( window ).trigger( 'pendingQueryCompleted', source );
                }
              });
            }
          })();

          (function() {
            var target = '#70209659b6af4980b17ef39884160406-pending-collapse';
            var count = $(target).data('pending-count');
            if (count > 0) {
              $.ajax({
                dataType: "json",
                crossDomain: true,
                url: 'http://localhost:8000/rabpubs/' + shortid + '/pending/wos',
                success:  function( data ) {
                  var source = '70209659b6af4980b17ef39884160406';
                  harvest.model.update( data, source );
                  $( window ).trigger( 'pendingQueryCompleted', source );
                }
              });
            }
          })();

          (function() {
            var target = '#c53746b63fe848bbac0a1ac0bf559b27-pending-collapse';
            var count = $(target).data('pending-count');
            if (count > 0) {
              $.ajax({
                dataType: "json",
                crossDomain: true,
                url: 'http://localhost:8000/rabpubs/' + shortid + '/pending/academic_analytics',
                success: function( data ) {
                  var source = 'c53746b63fe848bbac0a1ac0bf559b27'
                  harvest.model.update( data, source );
                  $( window ).trigger( 'pendingQueryCompleted', source );
                }
              });
            }
          })();
	};

	return {
		initModule : initModule
	};
}());
