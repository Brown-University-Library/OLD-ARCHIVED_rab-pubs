harvest.model = (function () {
	var

		configMap = {},

		stateMap  = {},

		update,
		pending,		
		initModule;

	pending_db = TAFFY();
	queries_db = TAFFY();

	update_pending = function ( data, source ) {
		data.forEach( function ( pendingObj ) {
			pendingObj.source = source;
			pending_db.insert( pendingObj );
		})
		$( window ).trigger( 'pendingQueryCompleted', source );
	};

	update_queries = function ( data, source ) {
		var params = data.params;
		queries_db.insert( {'source': source, 'params': params, 'new': true });
		var queries = data.queries;
		queries.forEach( function ( queryObj ) {
			queryObj.source = source;
			queries_db.insert( queryObj );
		})
		$( window ).trigger( 'queriesQueryCompleted', source );
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
			get, all, initialize;

		get = function ( paramObj ) {
			var data;

			data = queries_db( paramObj ).first();
			return data;
		};

		all = function ( paramObj ) {
			var data;

			data = queries_db( paramObj ).get();
			return data;
		}

		initialize = function ( sourceRabid ) {
			harvest.data.getQueries( sourceRabid );
		}

		return {
			get : get,
			all : all,
			initialize : initialize
		}
	}());

	initModule = function () {};

	return {
		initModule : initModule,
		pending : pending,
		queries : queries,
		update_queries : update_queries,
		update_pending : update_pending
	};
}());