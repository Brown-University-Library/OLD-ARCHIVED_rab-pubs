harvest.data = (function () {

	var
		configMap = {
			resource_base : "http://vivo.brown.edu/individual/",
			api_base : null,
      shortid : null
		},

    get,
    getPending,
		initModule, configModule;

	configModule = function ( config ) {
		configMap.api_base = config.api_base;
	};

  getPending = function( source ) {
    $.ajax({
      dataType: "json",
      crossDomain: true,
      url: 'http://localhost:8000/rabpubs/' + configMap.shortid + '/pending/' + source,
      success: function( data ) {
        harvest.model.update_pending( data, source );
      }
    });
  };

  getQueries = function( source ) {
    $.ajax({
      dataType: "json",
      crossDomain: true,
      url: 'http://localhost:8000/rabpubs/' + configMap.shortid + '/queries/' + source,
      success: function( data ) {
        harvest.model.update_queries( data, source );
      }
    });
  };

	initModule = function ( shortid ){
    configMap.shortid = shortid;
  };

	return {
    getPending : getPending,
    getQueries : getQueries,
    configModule : configModule,
		initModule : initModule
	};
}());
