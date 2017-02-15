harvest.data = (function () {

	var
		configMap = {
			resource_base : "http://vivo.brown.edu/individual/",
			app_base : null,
      shortid : null
		},

    get,
    getPending, getQueries,
    postQuery,
		initModule, configModule;

	configModule = function ( config ) {
    configMap.shortid = config.short_id;
		configMap.app_base = config.app_base;
	};

  getPending = function( source ) {
    $.ajax({
      dataType: "json",
      crossDomain: true,
      url: configMap.app_base + configMap.shortid + '/pending/' + source,
      success: function( data ) {
        harvest.model.update_pending( data, source );
      }
    });
  };

  getQueries = function( source ) {
    $.ajax({
      dataType: "json",
      crossDomain: true,
      url: configMap.app_base + configMap.shortid + '/harvest/' + source,
      success: function( data ) {
        harvest.model.update_queries( data, source );
      }
    });
  };

  postQuery = function( source, postData ) {
    $.ajax({
      method: "POST",
      data: JSON.stringify(postData),
      contentType:"application/json; charset=utf-8",
      dataType: "json",
      crossDomain: true,
      url: configMap.app_base + configMap.shortid + '/harvest/' + source,
      success: function( respData ) {
        console.log(respData);
        // harvest.model.update_queries( data, source );
      }
    });
  };

	initModule = function () {};

	return {
    getPending : getPending,
    getQueries : getQueries,
    postQuery : postQuery,
    configModule : configModule,
		initModule : initModule
	};
}());
