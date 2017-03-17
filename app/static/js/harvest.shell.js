harvest.shell = (function () {
	//---------------- BEGIN MODULE SCOPE VARIABLES --------------
	var
		
    stateMap	= {
      $container : undefined
    },
		
    jqueryMap = {},
    onPendingQueryCompleted,
    onQueriesQueryCompleted,
    onLaunchPendingModal,
    onLaunchProcessModal,
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

  onLaunchPendingModal = function ( pendingObj ) {
    harvest.modal.launchPendingDetail( pendingObj );
  };

  onLaunchProcessModal = function ( processObj, sourceObj ) {
    harvest.modal.launchProcessDetail( processObj, sourceObj.params );
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
      sources_model : harvest.model.sources
    });
    harvest.queries.initModule( jqueryMap.$container );

    harvest.modal.initModule( jqueryMap.$container );

    $( window ).on( 'pendingQueryCompleted', function( e, source ) {
      onPendingQueryCompleted( source );
    });

    $( window ).on( 'queriesQueryCompleted', function( e, source) {
       onQueriesQueryCompleted( source );
    });

    $( window ).on( 'launchPendingModal', function( e, pendingObj ) {
      onLaunchPendingModal( pendingObj );
    });

    $( window ).on( 'launchProcessModal', function( e, paramList ) {
      onLaunchProcessModal( paramList[0], paramList[1] );
    });

  };
  return { initModule : initModule };
  //------------------- END PUBLIC METHODS ---------------------
}());
