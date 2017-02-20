harvest.shell = (function () {
	//---------------- BEGIN MODULE SCOPE VARIABLES --------------
	var
		
    stateMap	= {
      $container : undefined
    },
		
    jqueryMap = {},
    onPendingQueryCompleted,
    onQueriesQueryCompleted,
		setJqueryMap, initModule;
	//----------------- END MODULE SCOPE VARIABLES ---------------
  //------------------- BEGIN UTILITY METHODS ------------------
  //-------------------- END UTILITY METHODS -------------------

  //--------------------- BEGIN DOM METHODS --------------------
  setJqueryMap = function () {
  	var $container = stateMap.$container;
  	jqueryMap = {
      $container : $container
    };
  };
  //---------------------- END DOM METHODS ---------------------
  //------------------- BEGIN EVENT HANDLERS -------------------
  //-------------------- END EVENT HANDLERS --------------------
  //---------------------- BEGIN CALLBACKS ---------------------
  onPendingQueryCompleted = function ( source ) {
    harvest.pending.loadPending( source );
  };

  onQueriesQueryCompleted = function ( source ) {
    harvest.queries.loadQueries( source );
  };

  //----------------------- END CALLBACKS ----------------------
  //------------------- BEGIN PUBLIC METHODS -------------------
  // Begin Public method /initModule/
  initModule = function ( $container ) {
  	// load HTML and map jQuery collections
  	stateMap.$container = $container;
  	setJqueryMap();


    // configure and initialize feature modules
    harvest.pending.configModule({
      pending_model : harvest.model.pending
    });
    harvest.pending.initModule( jqueryMap.$container );

    harvest.queries.configModule({
      queries_model : harvest.model.queries,
      params_model : harvest.model.params
    });
    harvest.queries.initModule( jqueryMap.$container );

    $( window ).on( 'pendingQueryCompleted', function( e, source ) {
      onPendingQueryCompleted( source );
    });

    $( window ).on( 'queriesQueryCompleted', function( e, source) {
       onQueriesQueryCompleted( source );
    });

  };
  return { initModule : initModule };
  //------------------- END PUBLIC METHODS ---------------------
}());
