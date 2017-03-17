harvest.model = (function () {
	var

		configMap = {},

		stateMap  = {},

		pending, update_pending,
		queries, update_queries,
		sources, update_sources,

		pending_db = TAFFY(),
		queries_db = TAFFY(),
    	sources_db = TAFFY(),

    	initModule;

	update_pending = function ( data, source ) {
		data.forEach( function ( pendingObj ) {
			pendingObj.source = source;
			pending_db.insert( pendingObj );
		})
		$( window ).trigger( 'pendingQueryCompleted', source );
	};

	update_queries = function ( data, source ) {
		data.forEach( function ( queryObj ) {
			queries_db.insert( { 	'rabid'	: queryObj.rabid,
						'id'	: queryObj.id,
						'source': queryObj.data.source[0],
						'data'	: queryObj.data,
						'display': queryObj.display } );
		});
		$( window ).trigger( 'queriesQueryCompleted', source );
	};

	update_sources = function ( sources ) {
		sources.forEach( function ( sourceObj ) {
			sources_db.insert( {	'rabid'	: sourceObj.rabid,
						'id'	: sourceObj.id,
						'params': sourceObj.data.parameters,
						'data'	: sourceObj.data,
						'display': sourceObj.display });
		});
	};

	pending = (function () {
		var
			get, all, initialize;

		get = function ( paramObj ) {
			var data;

			data = pending_db( paramObj ).first();
			return data;
		};

		all = function ( paramObj ) {
			var data;

			data = pending_db( paramObj ).get();
			return data;
		}

		initialize = function ( sourceRabid ) {
			harvest.data.getPending( sourceRabid );
		}

		return {
			get : get,
			all : all,
			initialize : initialize
		}
	}());

	queries = (function () {
		var
			get, all,
			create,
			initialize;

		get = function ( paramObj ) {
			var data;

			data = queries_db( paramObj ).first();
			return data;
		};

		all = function ( paramObj ) {
			var data;

			data = queries_db( paramObj ).get();
			return data;
		};

		create = function ( sourceRabid, dataObj ) {
			harvest.data.postQuery( sourceRabid, dataObj);
		};

		save = function ( sourceRabid, dataObj ) {

		};

		initialize = function ( sourceRabid ) {
			harvest.data.getQueries( sourceRabid );
		};

		return {
			get : get,
			all : all,
			create: create,
			initialize : initialize
		};
	}());

	sources = (function () {
		var
			get, all,
			create,
			initialize;

		get = function ( paramObj ) {
			var data;

			data = sources_db( paramObj ).first();
			return data;
		};

		all = function ( paramObj ) {
			var data;

			data = sources_db( paramObj ).get();
			return data;
		};

		return {
			get : get,
			all : all,
		};
	}());

	initModule = function ( sources ) {
		update_sources (sources );
	};

	return {
		initModule : initModule,
		pending : pending,
		queries : queries,
		sources : sources,
		update_queries : update_queries,
		update_pending : update_pending
	};
}());
